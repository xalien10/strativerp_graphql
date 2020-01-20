from datetime import date, timedelta, datetime

from django.db import transaction

from project.models import Project, ProjectEmployee
from reporting.models import ReportedHour
from user.models import User
from utils.helper import get_obj_or_none


@transaction.atomic
def merge_all_report_hour_multiple_entry():
    datetime_from = datetime(2019, 1, 1)
    date_from = datetime_from.date()
    today_now = datetime.now()
    today = date.today()
    all_projects = Project.objects.filter(status=Project.ACTIVE)
    for project_obj in all_projects:
        project_employee_group = ProjectEmployee.objects.filter(project=project_obj)

        for project_employee_obj in project_employee_group:
            days_to_subtract = 0
            # creator_user = get_obj_or_none(User, employees=[project_employee_obj.employee])
            creator_user = project_employee_obj.employee.user
            itr_date = today
            while itr_date >= date_from:
                total_reported_hour = 0
                total_reported_minutes = 0
                logged_hour_accumulated_description = ''

                itr_date_time = today_now - timedelta(days=days_to_subtract)
                days_to_subtract += 1
                itr_date = itr_date_time.date()

                project_reported_hours_by_date = ReportedHour.objects.filter(project_employee=project_employee_obj,
                                                                             date=itr_date)

                if project_reported_hours_by_date.count() > 1:
                    for single_reported_hour in project_reported_hours_by_date:
                        total_reported_hour += single_reported_hour.hours
                        total_reported_minutes += single_reported_hour.minute
                        logged_hour_accumulated_description += ' {} \n'.format(single_reported_hour.description)

                        single_reported_hour.delete()
                    total_reported_hour += (total_reported_minutes // 60)
                    total_reported_minutes = total_reported_minutes % 60

                    new_reported_hour_obj = {
                        'project_employee': project_employee_obj,
                        'date': itr_date,
                        'hours': total_reported_hour,
                        'minute': total_reported_minutes,
                        'description': logged_hour_accumulated_description,
                        'created_by': creator_user
                    }
                    new_reported_hour_obj = ReportedHour.objects.create(**new_reported_hour_obj)

    return 'Completed'
