from datetime import datetime, date

from jira import JIRA
import re
import pytz

utc = pytz.UTC

options = {
    'server': 'https://strativ.atlassian.net'
}
jira = JIRA(options, basic_auth=('apon@strativ.se', 'oC1l5UJEZS1gege7ZjJe2BCC'))


def get_all_jira_projects():
    projects = jira.projects()
    return projects


def get_issue_project_by_key(project_key):
    project = jira.project(project_key)
    return project


def get_issue_by_key(issue_key):
    issue = jira.issue(issue_key)
    return issue


def get_all_jira_users():
    project_keys = get_all_jira_projects()
    jira_users = jira.search_assignable_users_for_projects(username='', projectKeys=project_keys)
    return jira_users


def get_logged_hour(jql_str, start_at=0, max_results=50, jira_user_filter='', validate_query=True, fields=None,
                    expand=None, project_type=None,
                    worklog_from=None, worklog_to=None, json_result=None):
    """ get logged hour in a date range of issues filtered by a jql query.
    Returns a custom dict of billable and non billable issues and total time of all issues"""
    non_billable_epic_key_group = ['SEA-35', 'SEA-59']
    issues = jira.search_issues(jql_str, startAt=start_at, maxResults=max_results, validate_query=validate_query,
                                fields=fields, expand=expand,
                                json_result=json_result)

    total_seconds_for_all_issues = 0
    total_non_billable_seconds = 0
    total_billable_seconds = 0
    wlf = utc.localize(date_string_to_datetime_first_hour(worklog_from)) if worklog_from else None
    wlt = utc.localize(date_string_to_datetime_last_hour(worklog_to)) if worklog_to else None
    non_billable_issues, billable_issues = [], []
    for issue in issues:
        wlogs = issue.fields.worklog.worklogs
        total_seconds = 0
        for wlog in wlogs:
            wlog_time = datetime.strptime(wlog.started, '%Y-%m-%dT%H:%M:%S.%f%z')

            is_summable = False
            if jira_user_filter and wlog.author.key == jira_user_filter:
                is_summable = True
            elif not jira_user_filter:
                is_summable = True

            if is_summable:
                if wlf and wlt and wlf <= wlog_time <= wlt:
                    total_seconds += wlog.timeSpentSeconds
                elif wlf and not wlt and wlf <= wlog_time:
                    total_seconds += wlog.timeSpentSeconds
                elif wlt and not wlf and wlog_time <= wlt:
                    total_seconds += wlog.timeSpentSeconds
                elif not wlf and not wlt:
                    total_seconds += wlog.timeSpentSeconds
            
            # if jira_user_filter and wlog.author.key != jira_user_filter:
            #     total_seconds -= wlog.timeSpentSeconds

        issue.fields.worklog.totalTimeSpentSeconds = total_seconds
        total_seconds_for_all_issues += total_seconds

        if (issue.fields.customfield_10005 and issue.fields.customfield_10005 in non_billable_epic_key_group) or (
                project_type == 'internal'):
            non_billable_issues.append(issue)
            total_non_billable_seconds += total_seconds
        else:
            billable_issues.append(issue)
            total_billable_seconds += total_seconds

    categorized_issues = {
        'non_billable_issues': non_billable_issues,
        'billable_issues': billable_issues,
        'total_non_billable_seconds': total_non_billable_seconds,
        'total_billable_seconds': total_billable_seconds,
        'total_seconds_for_all_issues': total_seconds_for_all_issues
    }

    return categorized_issues


def date_string_to_datetime_last_hour(date_inp):
    if not isinstance(date_inp, str):
        date_inp = str(date_inp)

    date_inp += ' 23:59:59'
    datetime_out = datetime.strptime(date_inp, '%Y-%m-%d %H:%M:%S')
    return datetime_out


def date_string_to_datetime_first_hour(date_inp):
    datetime_out = datetime.strptime(date_inp, '%Y-%m-%d')
    return datetime_out


def append_jql_param(jql_str='', param_str=''):
    """ takes jql query_str and param_str returns full_jql_str"""
    if jql_str and param_str:
        jql_out = '{} AND {}'.format(jql_str, param_str)
    else:
        jql_out = jql_str or param_str or ''
    return jql_out
