"""api example to search for field names in a given document by key"""

# our helpers
import oauth2_wrappers

def main():
    """example code lives in one function"""
    # grab a token
    token = oauth2_wrappers.gen_token()

    # this is a document key
    # can take another from a script like document_search.py
    the_key = ('source=US SEC/filer=0001002242/docType=20-F/A/accession number='
               '0001174947-18-000616/theDate:20171231||filingDateTime:'
               '2018-04-13T13:33:50||file number:001-14090')

    # build a simple query dict
    query_dict = {'documentKey' : the_key}

    # api url stub
    api_url = 'docfieldnames'

    # send off the request
    resp_data = oauth2_wrappers.df_post(api_url, token, query_dict, {})

    # and iterate over the whole list of names
    for each_name in resp_data['fieldNames']:
        print(str(each_name))

main()

# eof
