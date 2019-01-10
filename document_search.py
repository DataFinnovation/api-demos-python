"""api example to search for documents by query string"""

# our helpers
import oauth2_wrappers

def main():
    """example code lives in one function"""
    # grab a token
    token = oauth2_wrappers.gen_token()

    # this is the query string we are going to run
    # the full query language is documented at:
    # https://userdocs.dfnapp.com/
    q_string_raw = '''
    companyname:(walmart OR "wal mart") AND 
    enddate:[2015-01-01 TO 2018-12-31] 
    AND filingsource:"US SEC"
    '''

    # urlencode the parameters
    # this is not the 'simple' query string so that is false
    # ensure the sortfield is a date or datetime
    # maxresult is an integer
    # sortascending is a boolean
    query_dict = {'querystring' : q_string_raw,
                  'simplequery' : False,
                  'maxresult' : 4,
                  'sortfield' : 'filingtime',
                  'sortascending' : False}

    # api url stub
    api_url = 'documents/textquery'

    # send off the request
    resp_data = oauth2_wrappers.df_get(api_url, token, query_dict)

    # process es results
    for ele in resp_data['hits']:
        doc_key = ele['source']['key']
        print('for key: '+str(doc_key))
        print('doc info is: '+str(ele['source']))

main()

# eof
