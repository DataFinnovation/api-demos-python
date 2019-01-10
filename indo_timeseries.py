"""builds a simple footnote feed for notable oil company entries"""

from oauth2_wrappers import gen_token
from df_wrappers import documents_stringquery, document_field_values

def main():
    """example code lives in one function"""

    # generate a token, we will be sending several queries off
    token = gen_token()

    # use the search string to find aces hardware indonesia
    # filings for the past 2 years
    doc_search_string = """
    filingsource:"Indonesia IDX" AND 
    filerid:"ACES" AND 
    enddate:[2017-01-01 TO 2018-12-31]
    """

    # send off the request
    # note we sort results by filing end date
    doc_data = documents_stringquery(doc_search_string, False,
                                     sortfield='enddate',
                                     sortascending=True,
                                     token=token)

    # this is the value we will extract from each doc
    field_tag = 'idx-cor:CurrentAssets'

    # iterate over ES results
    for ele in doc_data['hits']:
        # grab the key and end date for this entry
        this_doc_key = ele['source']['key']
        this_end_date = ele['source']['enddate']

        # send off the query
        res = document_field_values(this_doc_key, [field_tag], token=token)
        # pull out the 'value' of this field
        this_value = res['fields'][field_tag][0]['value']

        # and print out, note they are already ordered
        print(str(this_end_date) + ' : ' + str(this_value))

main()

# eof
