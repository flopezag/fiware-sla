from core.jiraconnector import Jira

if __name__ == "__main__":
    jira_instance = Jira()

    # output = \
    #    jira_instance.filter_issue(a_issue=jira_instance.jira.issue('HELP-13096', expand='changelog'))

    # print(output)

    issues = jira_instance.get_issues()

    print(len(issues))

    result = map(jira_instance.filter_issue, issues)

    print(len(result))

    solution_data = jira_instance.calculate_statistics(result)

    print(solution_data)
    