"""
fields related to the tax cuts and jobs act of 2017
related to periods ending in 2017
and filed in 2018
"""

from df_wrappers import facts_stringquery

def main():
    """example code lives in one function"""

    # this one is easier in the script language
    query_string = """
    filingsource:"US SEC" AND
    enddate:[2017-01-01 TO 2017-12-31] AND 
    filingtime:[2018-01-01 TO 2018-12-31] AND 
    fieldname:"tax cuts and jobs act"
    """

    # send off the query
    resp_data = facts_stringquery(query_string, False, maxresult=100000)
    # keep unique list of company names from results
    for item in resp_data['hits']:
        print(item['source']['companyname'] +
              ' filed a field called: ' +
              item['source']['fieldname'])

main()

# eof
