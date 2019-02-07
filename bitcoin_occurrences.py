"""counts filings and filers with bitcoin in them"""

import datetime

from df_wrappers import facts_dslquery

def main():
    """example code lives in one function"""

    for year in range(2013, 2019):
        # set up boundary dates
        start_date = datetime.datetime(year, 1, 1)
        end_date = datetime.datetime(year+1, 1, 1)
        start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
        end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')

        # query params
        params = {'maxresult' : 1000}
        # es ds query
        dsl_dict = {
            "query": {
                "constant_score" : {
                    "filter" : {
                        "bool" : {
                            "must" : [
                                {"terms" : {"fieldname": ["bitcoin",
                                                          "cryptocurrency"]}},
                                {"range" : {"enddate" : {"gte" : start_str,
                                                         "lt" : end_str}}},
                                {"terms" : {"filingsource" : ["US SEC"]}}
                            ]
                        }
                    }
                }
            }
        }

        # send off the query
        resp_data = facts_dslquery(dsl_dict, params=params)
        # keep unique list of company names from results
        companies = []
        for hit in resp_data['hits']:
            companies.append(hit['source']['companyname'])
        companies = list(set(companies))
        print(str(year)+','+str(resp_data['totalHits'])+','+str(len(companies)))

main()

# eof
