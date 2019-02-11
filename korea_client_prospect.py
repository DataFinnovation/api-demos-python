"""the names of companies which filed fields with certain words in them"""

from df_wrappers import facts_stringquery

def main():
    """example code lives in one function"""

    # this one is easier in the script language
    query_string = """
    filingsource:"Korea FSS" AND
    fieldname:(hedge OR (foreign AND exchange) OR (interest AND rate))
    """

    # send off the query
    resp_data = facts_stringquery(query_string, False)
    # keep unique list of company names from results
    name_list = {x['source']['companyname'] for x in resp_data['hits']}
    for name in name_list:
        print(str(name))

main()

# eof
