"""
a two-pass example
first identify companies with likely interesting esg characteristics
by filtering for those that have filed fields about coal or hydro

then find all text fields containing the word environment for
that list of companies
"""

from df_wrappers import facts_dslquery

def main():
    """example query"""

    start_date = "2018-01-01"
    end_date = "2018-06-30"

    # first pass to find fields about coal or hydro
    first_query = {
        "query" : {
            "constant_score" : {
                "filter" : {
                    "bool" : {
                        "must" : [
                            {"term" : {"filingsource" : "US SEC"}},
                            {"terms" : {"fieldname" : ["coal", "hydro"]}},
                            {"range" : {"filingtime" : {"gte" : start_date,
                                                        "lt" : end_date}}}
                        ]
                    }
                }
            }
        }
    }
    res = facts_dslquery(first_query, params={'maxresult' : 10000})

    # now distill down to a list of company names and a big OR query
    companies = {hit['source']['companyname'] for hit in res['hits']}
    company_query_string = "companyname:(" + " OR ".join(['"'+x+'"' for x in companies]) + ")"

    # second pass for those companies find environment-related text content
    second_query = {
        "query" : {
            "constant_score" : {
                "filter" : {
                    "bool" : {
                        "must" : [
                            {"term" : {"filingsource" : "US SEC"}},
                            {"query_string" : {"query" : company_query_string}},
                            {"wildcard" : {"fieldname" : "*environment*"}},
                            {"range" : {"filingtime" : {"gte" : start_date,
                                                        "lt" : end_date}}}
                        ],
                        "must_not" : [
                            {"exists" : {"field" : "units"}},
                        ]
                    }
                }
            }
        }
    }

    # and iterate through
    res2 = facts_dslquery(second_query, params={'maxresult' : 1000})
    for hit in res2['hits']:
        cname = hit['source']['companyname']
        fieldname = hit['source']['fieldname']
        fieldvalue = hit['source']['fieldvalue']
        print(cname + 'filed a '+ fieldname + " containing:")
        print(fieldvalue)

main()

# eof
