import sys
from jira import JIRA
from datetime import datetime
from datetime import timedelta


username = sys.argv[1]
password = sys.argv[2]
#jql_query = 'project = "OSS SM" AND issuetype in (Bug, TR) AND "Feature Areas" = "EO SO" AND createdDate >= startOfYear()'
jql_query = 'project = "OSS SM" AND issuetype in (Bug, TR) AND "Feature Areas" = "EO SO" AND createdDate >= startOfYear() AND resolution != Fixed'

jira = JIRA('https://jira-oss.seli.wh.rnd.internal.ericsson.com',
            auth=(username, password))

issues_matching_query = jira.search_issues(jql_query, startAt=0, maxResults=500)


def get_time_open(issue):
    creation_time = issue.fields.created
    resolved_time = issue.fields.resolutiondate
    createdTime = datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S.%f%z')
    resolvedTime = datetime.strptime(resolved_time, '%Y-%m-%dT%H:%M:%S.%f%z')
    duration = resolvedTime - createdTime
    return duration


def resolved(issue):
    if hasattr(issue.fields, 'resolutiondate'):
        if issue.fields.resolutiondate is not None:
            return True
    else:
        return False


resolved_issues_duration = {}
for issue in issues_matching_query:
    print('Issue {} created on {}'.format(issue.key, issue.fields.created))
    if resolved(issue):
        resolved_issues_duration[issue.key] = get_time_open(issue)

total_open_time = sum(resolved_issues_duration.values(), timedelta())
number_of_issues = len(resolved_issues_duration)
average_duration_of_issues = total_open_time / number_of_issues
print('Total open time of {} issues was {}'.format(number_of_issues, total_open_time))
print(average_duration_of_issues)