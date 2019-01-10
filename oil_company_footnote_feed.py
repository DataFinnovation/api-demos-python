"""builds a simple footnote feed for notable oil company entries"""

from df_wrappers import facts_dslquery

def main():
    """example code lives in one function"""

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
                            {"terms" : {"companyname": ["exxon", "chevron",
                                                        "bp", "shell",
                                                        "phillips"]}},
                            {"terms" : {"fieldvalue": ["litigation",
                                                       "lawsuit",
                                                       "damages",
                                                       "spill",
                                                       "explosion"]}},
                            {"range" : {"retrievaltime" : {"gte" : "now-180d/d",
                                                           "lt" : "now/d"}}}
                        ]
                    }
                }
            }
        }
    }

    # send off the query
    resp_data = facts_dslquery(dsl_dict)

    # and iterate over all the elasticsearch hits
    for ele in resp_data['hits']:
        print(ele)

main()

# eof
