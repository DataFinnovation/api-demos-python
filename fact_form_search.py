"""api example to search for facts by the form interface"""

# our helpers
import oauth2_wrappers

def main():
    """example code lives in one function"""
    # grab a token
    token = oauth2_wrappers.gen_token()

    # set up our simple query string
    # 
    # field names and matchTypes are documented at
    # https://app.swaggerhub.com/apis-docs/datafinnovation/clientapi/1.0/
    query_dict = {
        "fields": {
            "companyname": {
                "type"      : "matchquery",
                "matchType" : "startsWith",
                "value"     : "ibm"
            }
        }
    }

    # and any query param
    q_params = {'maxresult' : 2}

    # the url stub we post to
    api_url = 'facts/formquery'

    # send off the request
    resp_data = oauth2_wrappers.df_post(api_url, token, query_dict, q_params)

    # and iterate over all the elasticsearch hits
    for ele in resp_data['hits']:
        print(ele)

main()

# eof
