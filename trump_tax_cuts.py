"""the names of companies which filed fields with certain words in them"""

from df_wrappers import facts_stringquery

def main():
    """example code lives in one function"""

    # this one is easier in the script language
    query_string = """
    filingsource:"US SEC" AND
    enddate:[2017-01-01 TO 2017-12-31] AND 
    fieldname:"tax cuts and jobs act"
    """

    # send off the query
    resp_data = facts_stringquery(query_string, False)
    # keep unique list of company names from results
    for item in resp_data['hits']:
        print(item['source']['companyname'] +
              ' filed a field called: ' +
              item['source']['fieldname'])

main()

# eof
