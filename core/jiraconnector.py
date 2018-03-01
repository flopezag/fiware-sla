from jira import JIRA
from dateutil import parser
import pytz
import datetime
import pandas as pd
from core.SLATime import SLATime
from config.settings import JIRA_USER, JIRA_PASSWORD, JIRA_QUERY, JIRA_URL


class Jira():
    def __init__(self):
        # By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
        # (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
        # Override this with the options parameter.
        options = {
            'server': JIRA_URL
        }

        self.jira = JIRA(options, basic_auth=(JIRA_USER, JIRA_PASSWORD))

        # Fetch all fields
        allfields = self.jira.fields()

        # Make a map from field name -> field id
        self.nameMap = {field['name']: field['id'] for field in allfields}

        self.total_issues = list()

    def filter_issue(self, a_issue):
        # print(a_issue.key)
        created = a_issue.fields.created
        resolved = a_issue.fields.resolutiondate
        hd_node = getattr(a_issue.fields, self.nameMap['HD-Node']).value

        changelog = a_issue.changelog

        progressed = [item.created for item in [history for history in changelog.histories]
                      if (item.items[0].field == 'status'
                          and (
                                (item.items[0].fromString == 'Open' and item.items[0].toString == 'In Progress')
                                or
                                (item.items[0].fromString == 'Open' and item.items[0].toString == 'Answered')
                          )
                      )]

        if len(progressed) == 0:
            # This is an issues that was dismissed, therefore the time should be calculate in a different way
            progressed = [item.created for item in [history for history in changelog.histories]
                          if (len(item.items) == 2
                              and
                              item.items[1].field == 'status'
                              and
                              item.items[1].fromString == 'Open' and item.items[1].toString == 'Closed'
                              )]

        t_created = parser.parse(created)

        t_now = pytz.utc.localize(datetime.datetime.utcnow())

        try:
            t_progressed = parser.parse(progressed[0])
            # time_response = (t_progressed - t_created).total_seconds()
            time_response = SLATime.office_time_between(t_created, t_progressed).total_seconds()
        except:
            # time_response = (t_now - t_created).total_seconds()
            time_response = SLATime.office_time_between(t_created, t_now).total_seconds()
            t_progressed = None

        try:
            t_resolved = parser.parse(resolved)
            # time_resolve = (t_resolved - t_created).total_seconds()
            time_resolve = SLATime.office_time_between(t_created, t_resolved).total_seconds()
        except:
            # time_resolve = (t_now - t_created).total_seconds()
            time_resolve = SLATime.office_time_between(t_created, t_now).total_seconds()
            t_resolved = None

        # print(created, progressed[0], resolved, unicode(t_created), unicode(t_progressed), unicode(t_resolved))
        return {'hd_node': hd_node, 'time_response': time_response, 'time_resolve': time_resolve}

    def calculate_statistics(self, a_list):
        solution = list()

        df = pd.DataFrame(a_list)

        print('\n')
        print(df)

        nodes = df['hd_node'].unique()

        print(nodes)

        for i in range(0, len(nodes)):
            df_aux = df[df['hd_node'] == nodes[i]]

            # print(series)
            print('\n')
            print(df_aux)
            number_time_resolve = df_aux['time_resolve'].count()
            number_time_response = df_aux['time_response'].count()

            # Quiero numero de datos, media, desviacion tipica y percentil de cada columna (time_resolve, time response)
            t1 = df_aux["time_resolve"].mean()
            t2 = df_aux["time_response"].mean()

            d1 = df_aux["time_resolve"].std()
            d2 = df_aux["time_response"].std()

            limit_response_time = 24 * 60 * 60
            limit_resolution_day = 2 * 24 * 60 * 60

            print('\ntime_response_mean: {}, deviation_response: {}'.format(t2, d2))
            print('time_resolve_mean: {}, deviation_resolve: {}'.format(t1, d1))

            print('\nlimit_response_time: {}, limit_resolution_day: {}'
                  .format(limit_response_time, limit_resolution_day))

            out1 = df_aux[df_aux['time_resolve'] <= limit_resolution_day]
            out2 = df_aux[df_aux['time_response'] <= limit_response_time]

            number_below_time_resolve = out1['time_resolve'].count()
            number_below_time_response = out2['time_response'].count()

            p_time_resolve = number_below_time_resolve * 1.0 / number_time_resolve * 100
            p_time_response = number_below_time_response * 1.0 / number_time_response * 100

            print(p_time_resolve)
            print(p_time_response)

            solution_list = {
                'FIWARE Lab node': nodes[i],
                'Number Issues': number_time_resolve,
                '% Issues responded <24h': p_time_response,
                '% Issues resolved <2d': p_time_resolve
            }

            solution.append(solution_list)

        solution_df = pd.DataFrame(solution)

        return solution_df

    def get_issues(self):
        block_size = 100
        block_num = 0

        while True:
            start_idx = block_num * block_size

            list_issues = \
                self.jira.search_issues(jql_str=JIRA_QUERY, startAt=start_idx, maxResults=block_size, expand='changelog')

            if len(list_issues) == 0:
                # Retrieve issues until there are no more to come
                break

            self.total_issues = self.total_issues + list_issues

            block_num += 1

            # print(len(list_issues))
            print(block_num)

        print(len(self.total_issues))

        return self.total_issues
