""" A simple admin script to find when the last filing arrived by source. """

import argparse
import datetime
import sys

from df_wrappers import documents_dslquery

def run_sources(source_list):
    """
    processes a list of source names
    """
    params = {'maxresult' : 1}
    source_date_pairs = []
    for source_name in source_list:
        dsl_query = {
            "query": {
                "term" : {
                    "filingsource": source_name
                }
            },
            "sort" : {'retrievaltime' : 'desc'}
        }

        # post the request
        resp_data = documents_dslquery(dsl_query, params=params)
        last_arrival_time = resp_data['hits'][0]['source']['retrievaltime']
        last_dt = datetime.datetime.strptime(last_arrival_time, '%Y-%m-%dT%H:%M:%S')
        source_date_pairs.append([source_name, last_dt])
    return source_date_pairs

def main(_):
    """
    main only parses args and passes along the parameters.
    we use _ as the argument name to maintain compatibility with our web
    development sandbox and appease pylint at the same time.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--cutoff', type=int, dest='cutoff', default=15,
                        help='how many days back to place the cutoff')
    args = parser.parse_args()

    source_name_list = ['US SEC', 'UK CH', 'Chile SVS',
                        'Peru SMV', 'Japan EDINET', 'Taiwan TWSE',
                        'Indonesia IDX', 'Spain CNMV', 'Korea FSS',
                        'India BSE', 'US SEC Non-XBRL']

    source_date_pairs = run_sources(source_name_list)

    # insert a placeholder to indicate what are likely fine results vs out of date
    now = datetime.datetime.utcnow()
    cutoff_date = now - datetime.timedelta(days=args.cutoff)
    cutoff_str = '   ---  '+str(args.cutoff)+' Days ---   '
    source_date_pairs.append([cutoff_str, cutoff_date])

    sorted_data = sorted(source_date_pairs, key=lambda x: x[1])

    for ele in sorted_data:
        the_dt = ele[1]
        days = (now - the_dt)
        ele.append(days)
        print(' : '.join([str(x) for x in ele]))

if __name__ == '__main__':
    main(sys.argv[1:])

# eof
