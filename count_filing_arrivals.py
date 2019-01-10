"""counts the number of filings for each month going back years"""

import calendar
import datetime

from oauth2_wrappers import gen_token
from df_wrappers import documents_dslquery

def main():
    """example code lives in one function"""

    # generate a token, we will be sending several queries off
    token = gen_token()

    # which source to count
    # mainly US SEC and Japan EDINET have large histories
    source_to_count = "US SEC"

    # this query filters for company names from a list
    # where field values contain a word off a list
    # filed in the last 180 days
    # this is all standard Elasticsearch DSL
    dsl_dict = {
        "query": {
            "constant_score" : {
                "filter" : {
                    "bool" : {
                        "must" : [
                            {"term" : {"filingsource": source_to_count}},
                            {"range" : {"filingtime" : {"gte" : "2018-01-01",
                                                        "lt" : "2018-01-31"}}}
                        ]
                    }
                }
            }
        }
    }
    # use a pointer to shorten the assignments below
    array_ref = dsl_dict["query"]["constant_score"]["filter"]["bool"]["must"][1]

    # set the number of returned results to 1
    # as all we care about is the totalHits entry anyway
    param_dict = {'maxresult' : 1}

    # print out csv headers
    print(','.join(['start date', 'end date', 'number filings']))
    for year in range(2010, 2020):
        for month in range(0, 12):
            # beginning of range
            start_date = datetime.datetime(year, month+1, 1)

            # if this is past today dont bother as surely 0
            if start_date > datetime.datetime.utcnow():
                continue
            start_date_str = start_date.strftime("%Y-%m-%d")

            # end of range
            last_day = calendar.monthrange(year, month+1)[1]
            end_date = datetime.datetime(year, month+1, last_day)
            end_date_str = end_date.strftime("%Y-%m-%d")

            # assign this date range
            array_ref["range"]["filingtime"]["gte"] = start_date_str
            array_ref["range"]["filingtime"]["lte"] = end_date_str

            # send off the query
            resp_data = documents_dslquery(dsl_dict, token=token, params=param_dict)

            # read the number of total matches from ES
            num_hits = resp_data['totalHits']

            # format and print the line
            res_list = [start_date_str, end_date_str, str(num_hits)]
            print(','.join(res_list))

main()

# eof
