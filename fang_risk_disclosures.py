"""
Example script which pulls risk disclosures for the FANG stocks.
"""

from df_wrappers import facts_dslquery

def main():
    """example query"""

    dsl_query = {
        "query" : {
            "constant_score" : {
                "filter" : {
                    "bool" : {
                        "must" : [
                            # Source for non-xbrl US SEC filings
                            {"term" : {"filingsource" : "US SEC Non-XBRL"}},
                            # Focus only on 10-Ks
                            {"match" : {"reporttype" : "10-K"}},
                            # We want section 1A
                            {"match" : {"fieldname" : "1A"}},
                            # use partial names to keep it short.  For real use probably better to
                            # rely on CIK as filerid.
                            {"terms" : {"companyname" : ['facebook', 'apple',
                                                         'netflix', 'google',
                                                         'alphabet']}}
                        ]
                    }
                }
            }
        }
    }

    res = facts_dslquery(dsl_query)

    for hit in res['hits']:
        # just print them out
        print(str(hit))

main()

# eof
