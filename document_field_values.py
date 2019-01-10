"""api example to search for field values key and label"""

# our helpers
import oauth2_wrappers

def main():
    """example code lives in one function"""
    # grab a token
    token = oauth2_wrappers.gen_token()

    # this is a document key
    # can take another from a script like document_search.py
    the_key = ('source=US SEC/filer=0001002242/docType=20-F/A/accession '
               'number=0001174947-18-000616/theDate:20171231||'
               'filingDateTime:2018-04-13T13:33:50||file number:001-14090')

    # these names are in that key
    # can take more from a script like document_field_names
    the_names = ['ifrs-full:InterestExpenseOnBonds',
                 'E:NonCurrentIncomeTaxReceivables']

    # build a the query dict
    query_dict = {'documentKey' : the_key,
                  'fieldNames' : the_names}

    # api url stub
    api_url = 'docfields'

    # send off the request
    resp_data = oauth2_wrappers.df_post(api_url, token, query_dict, {})

    # iterate over each returned field
    for each_name in resp_data['fields']:
        # and over each entry for that field
        for each_entry in resp_data['fields'][each_name]:
            # print out a single fact entry
            print(str(each_entry))

main()

# eof
