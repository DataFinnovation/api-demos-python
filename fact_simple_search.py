"""api example to search for facts by simple query string"""

# our helpers
import oauth2_wrappers

def main():
    """example code lives in one function"""
    # grab a token
    token = oauth2_wrappers.gen_token()

    # set up our simple query string
    # the full query language is documented at:
    # https://userdocs.dfnapp.com/
    query_string_raw = '+exxon +litigation +2018'
    query_dict = {'querystring' : query_string_raw,
                  'simplequery' : True}

    # url stub
    api_url = 'facts/textquery'

    # send off the request
    resp_data = oauth2_wrappers.df_get(api_url, token, query_dict)

    # and iterate over all the elasticsearch hits
    for ele in resp_data['hits']:
        print(ele)

main()

# eof
