import decimal
from datetime import datetime, date, timedelta, time
from django.utils import timezone
from core.utils.jira_utils import append_jql_param, get_logged_hour
from payroll.models import Salary
from project.models import ProjectEmployee, Project
from reporting.models import ReportedHour
from user.models import User
from utils.helper import get_obj_or_none


def insert_logged_jira_hours_into_erp():
    res = str(datetime.now())
    print('scheduled job ran at - {}'.format(res))
    return res


def jira_hour_sync_to_erp(jira_project_key_filter=None, jira_user_key_filter=None,
                          date_from_filter=None, date_to_filter=None):
    if not date_from_filter or not date_to_filter:
        date_from_filter = datetime.today().date()
        date_to_filter = datetime.today().date()
    try:
        all_projects = Project.objects.filter(status=Project.ACTIVE).exclude(jira_project_key=None)
        if jira_project_key_filter:
            all_projects = all_projects.filter(jira_project_key=jira_project_key_filter)
        for project_obj in all_projects:
            project_employee_group = ProjectEmployee.objects.filter(project=project_obj, status=ProjectEmployee.ACTIVE)
            for project_employee_obj in project_employee_group:
                jira_user_key = getattr(User.objects.get(employees=project_employee_obj.employee), 'jira_user_key')
                if jira_user_key_filter and jira_user_key_filter != jira_user_key:
                    continue

                jira_project_key = project_obj.jira_project_key

                user = get_obj_or_none(User, jira_user_key=jira_user_key)
                project_employee = get_obj_or_none(
                    ProjectEmployee,
                    project__jira_project_key=jira_project_key,
                    employee__user=user,
                )
                if not jira_user_key or not jira_project_key or not user or not project_employee:
                    continue

                itr_days = 0
                itr_date = date_from_filter

                project_hourly_income = project_employee.project.income
                employee_hourly_income = Salary.objects.get(employee=project_employee_obj.employee)
                employee_hourly_income = employee_hourly_income.amount

                while itr_date <= date_to_filter:
                    jql = ''
                    issue_description = ''
                    itr_date_str = str(itr_date)

                    jql_jira_project_param = 'project="{}"'.format(jira_project_key)
                    jql = append_jql_param(jql, jql_jira_project_param)
                    jql_worklog_date_param = 'worklogDate="{}"'.format(itr_date_str)
                    jql = append_jql_param(jql, jql_worklog_date_param)
                    jql_jira_assignee_param = 'assignee="{}"'.format(jira_user_key)
                    jql = append_jql_param(jql, jql_jira_assignee_param)

                    categorized_issues = get_logged_hour(jql, jira_user_filter=jira_user_key, worklog_from=itr_date_str,
                                                         worklog_to=itr_date_str,
                                                         project_type=project_obj.project_type,
                                                         fields=['summary', 'status', 'assignee', 'issuetype',
                                                                 'priority', 'status', 'worklog', 'customfield_10005'])

                    billable_issues = categorized_issues.get('billable_issues')
                    total_billable_time = categorized_issues.get('total_billable_seconds')
                    total_billable_hr = decimal.Decimal(total_billable_time / 3600)

                    non_billable_issues = categorized_issues.get('non_billable_issues')
                    total_non_billable_time = categorized_issues.get('total_non_billable_seconds')
                    total_non_billable_hr = decimal.Decimal(total_non_billable_time / 3600)

                    # Billable hour report create or update
                    for issue in billable_issues:
                        issue_description += '{} - {} \n'.format(issue.fields.summary, issue.key)
                    hr = total_billable_time // 3600
                    mn = (total_billable_time % 3600) / 60
                    billable_reported_hour_income = project_hourly_income * total_billable_hr
                    billable_reported_hour_cost = employee_hourly_income * total_billable_hr
                    billable_reported_hour_profit = billable_reported_hour_income - billable_reported_hour_cost

                    new_billable_reported_hour = {
                        #should be comented from here
                        'income': billable_reported_hour_income,
                        'cost': billable_reported_hour_cost,
                        'profit': billable_reported_hour_profit,
                        # to here asap and uncomment the else part as well
                        'hours': hr,
                        'minute': mn,
                        'description': issue_description,
                        'created_by': user
                    }

                    if hr or mn:
                        reported_hour, is_created = ReportedHour.objects.get_or_create(
                            defaults=new_billable_reported_hour,
                            project_employee=project_employee, date=itr_date, is_billable=True)

                        if not is_created:
                            for key, val in new_billable_reported_hour.items():
                                setattr(reported_hour, key, val)
                            reported_hour.updated_by = user
                            reported_hour.updated_at = timezone.now()
                            reported_hour.save()
                        # should be uncommented after running a sync once from 23-sept-2019 till today
                        # else:
                        #     reported_hour.income = billable_reported_hour_income,
                        #     reported_hour.cost = billable_reported_hour_cost,
                        #     reported_hour.profit = billable_reported_hour_profit,
                        #     reported_hour.save()

                    # Non billable hour report create or update
                    issue_description = ''
                    non_billable_reported_hour_income = project_hourly_income * total_non_billable_hr
                    non_billable_reported_hour_cost = employee_hourly_income * total_non_billable_hr
                    non_billable_reported_hour_profit = non_billable_reported_hour_income - non_billable_reported_hour_cost

                    for issue in non_billable_issues:
                        issue_description += '{} - {} \n'.format(issue.fields.summary, issue.key)
                    hr = total_non_billable_time // 3600
                    mn = (total_non_billable_time % 3600) / 60
                    new_non_billable_reported_hour = {
                        # should be comented from here
                        'income': non_billable_reported_hour_income,
                        'cost': non_billable_reported_hour_cost,
                        'profit': non_billable_reported_hour_profit,
                        # to here asap and uncomment the else part as well
                        'hours': hr,
                        'minute': mn,
                        'description': issue_description,
                        'created_by': user
                    }

                    if hr or mn:
                        reported_hour, is_created = ReportedHour.objects.get_or_create(
                            defaults=new_non_billable_reported_hour,
                            project_employee=project_employee, date=itr_date, is_billable=False)

                        if not is_created:
                            for key, val in new_non_billable_reported_hour.items():
                                setattr(reported_hour, key, val)
                            reported_hour.updated_by = user
                            reported_hour.updated_at = timezone.now()
                            reported_hour.save()
                        # should be uncommented after running a sync once from 23-sept-2019 till today
                        # else:
                        #     reported_hour.income = non_billable_reported_hour_income,
                        #     reported_hour.cost = non_billable_reported_hour_cost,
                        #     reported_hour.profit = non_billable_reported_hour_profit,
                        #     reported_hour.save()

                    itr_days += 1
                    itr_date_time = datetime.combine(date_from_filter, time(hour=0, minute=0, second=0)) + timedelta(
                        days=itr_days)
                    itr_date = itr_date_time.date()

        time_now = str(datetime.now())
        print('jira hour sync job ran at - {}. [Successful]'.format(time_now))
        return 'successful'

    except Exception as e:
        time_now = str(datetime.now())
        print('jira hour sync job ran at - {}. [Exeption] - {}'.format(time_now, str(e)))
        return e
