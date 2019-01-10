"""api example to search for facts by query string"""

# our helpers
import oauth2_wrappers

def main():
    """example code lives in one function"""
    # grab a token
    token = oauth2_wrappers.gen_token()

    # this is the query string we are going to run
    # the full query language is documented at:
    # https://userdocs.dfnapp.com/
    # and
    # https://www.elastic.co/guide/en/elasticsearch/reference/6.3/query-dsl-query-string-query.html#query-string-syntax
    q_string_raw = 'companyname:(exxon OR chevron) AND fieldvalue:litigation'

    # urlencode the parameters
    # this is not the 'simple' query string so that is false
    q_dict = {'querystring' : q_string_raw,
              'simplequery' : False}

    # this api url stub
    api_url = 'facts/textquery'

    # send off the request
    resp_data = oauth2_wrappers.df_get(api_url, token, q_dict)

    # and iterate over all the elasticsearch hits
    # that format is documented at:
    # https://www.elastic.co/guide/en/elasticsearch/reference/6.3/search-request-body.html
    for ele in resp_data['hits']:
        print(ele)

main()

# eof
