"""api example to search for facts by ES DSL"""

# our helpers
import oauth2_wrappers

def main():
    """example code lives in one function"""

    # grab a token
    token = oauth2_wrappers.gen_token()

    # this is the elasticsearch dsl query we want to run
    # field names are documented at:
    # https://userdocs.dfnapp.com/
    # the query dsl is documented at:
    # https://www.elastic.co/guide/en/elasticsearch/reference/6.3/query-dsl.html
    dsl_query = {
        "query": {
            "term" : {
                "companyname": "microsoft"
            }
        }
    }
    dsl_dict = {'dslquery' : dsl_query}

    # and any query params
    query_dict = {'maxresult' : 2}

    # the url stub we post to
    api_url = 'facts/dslquery'

    # post the request
    resp_data = oauth2_wrappers.df_post(api_url, token, dsl_dict, query_dict)

    # and iterate over all the elasticsearch hits
    for ele in resp_data['hits']:
        print(ele)

main()

# eof
