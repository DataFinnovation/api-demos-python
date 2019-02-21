"""
demo that retrieves fields in japanese and then runs google translate
to english
"""

from googletrans import Translator

from df_wrappers import facts_dslquery

def main():
    """example query"""

    dsl_query = {
        "query" : {
            "constant_score" : {
                "filter" : {
                    "bool" : {
                        "must" : [
                            {"term" : {"filingsource" : "Japan EDINET"}},
                            {"term" : {"fieldtag" : "jpcrp_cor:addressmajorshareholders"}},
                            {"range" : {"filingtime" : {"gte" : "2018-01-01",
                                                        "lt" : "2018-01-15"}}}
                        ]
                    }
                }
            }
        }
    }

    res = facts_dslquery(dsl_query)

    trans = Translator()
    for hit in res['hits']:
        # grab the field contents
        this_value = hit['source']['fieldvalue']
        # and translate it
        t_value = trans.translate(this_value, src='ja', dest='en')
        # print that out
        print(t_value)

main()

# eof
