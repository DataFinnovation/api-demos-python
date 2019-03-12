"""wrapper functions around requests to help with oauth2"""

# basic oauth2 wrappers
# at a minimum we require requests on top of the standard library
# if oauthlib and requests_oauthlib are also present
# we run on top of them.
# error handling in the basic wrappers is limited for clarity
# for production uses build on top of some oauth2 package

import json
import os
from urllib.parse import urlencode
import requests

# if these packages are available use them
# otherwise go with some simple code
try:
    import oauthlib
    import requests_oauthlib
    HAVE_DEPS = True
except ImportError as _:
    HAVE_DEPS = False

# grab these from the environment
# feel free to set directly if you prefer
CLIENT_ID = os.environ['DF_CLIENT_ID']
CLIENT_SECRET = os.environ['DF_CLIENT_SECRET']
API_KEY = os.environ['DF_API_KEY']

# url to generate access tokens
# these are documented at http://webclient.dfnapp.com/ where
# you set up client ids and secrets
TOKEN_URL = 'https://apiauth.dfnapp.com/oauth2/token'

# api url starting stub
API_URL_STUB = 'https://clientapi.dfnapp.com/'

# full list of scopes
# note that you may not be permissioned for all scopes for all logins
DEFAULT_SCOPE = 'clientapi/basicsearch clientapi/advancedsearch'

# simple wrapper that builds the required headers
# this includes both our (transient) access token and
# the api key
def bearer_auth_headers(token):
    """simple wrapper to build the bearer-token authorization headers"""
    headers = {'Authorization' : 'Bearer '+token,
               'Content-Type' : 'application/json',
               'x-api-key' : API_KEY}
    return headers

# this does not include detailed error handling etc
# but is intended for use when oauthlib and requests_oauthlib are
# not available.
def gen_token_base(scope=DEFAULT_SCOPE):
    """simple code to generate an auth token"""
    # build a basic auth object
    the_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

    # this header is needed to generate a token
    headers = {'Content-Type' : 'application/x-www-form-urlencoded'}

    # the required grant type and scope(s)
    body = {
        'grant_type' : 'client_credentials',
        'scope' : scope
    }

    # send off the post request
    resp = requests.post(
        TOKEN_URL,
        auth=the_auth,
        data=body,
        headers=headers
    )

    # read back, and pull out the right dictionary entry
    resp_dict = json.loads(resp.content)
    the_token = resp_dict['access_token']
    return the_token

def gen_token_deps(scope=DEFAULT_SCOPE):
    """this version is built around more capable libraries"""
    # basic object setup
    client = oauthlib.oauth2.BackendApplicationClient(client_id=CLIENT_ID)
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

    # prep the oauth2 request
    oauth = requests_oauthlib.OAuth2Session(client=client, scope=scope)

    # grab the token and return it
    token = oauth.fetch_token(token_url=TOKEN_URL, auth=auth)
    return token['access_token']

def gen_token(**kwargs):
    """token generating wrapper, handles dependency availability"""

    # sort out scope, use default if nothing is provided
    scope = kwargs.get('scope', DEFAULT_SCOPE)

    # if the imports did not work then fall back on a basic implementation
    # otherwise use the good one
    if not HAVE_DEPS:
        return gen_token_base(scope)
    return gen_token_deps(scope)

def append_query_dict_to_url(url_in, query_dict):
    """encode query dict and append to url"""
    encoded_dict = urlencode(query_dict)
    full_url = url_in + '?' + encoded_dict
    return full_url

def df_get(url, token, query_dict):
    """wrapper for requests.get which handles bearer oauth2 tokens"""
    # generate url, bearer headers, send request and decode result
    full_url = API_URL_STUB + append_query_dict_to_url(url, query_dict)
    headers = bearer_auth_headers(token)
    resp = requests.get(full_url, headers=headers)
    resp_data = json.loads(resp.content)

    # read back the result
    if resp.status_code == requests.codes.ok:
        return resp_data
    raise ValueError('got an error loading: '+str(resp) +
                     '\n' + str(resp_data))

def df_post(url, token, data, query_dict):
    """wrapper for requests.post which handles bearer oauth2 tokens"""
    # generate url, bearer headers, send request and decode result
    # note that we json-encode the dict for posting
    full_url = API_URL_STUB + append_query_dict_to_url(url, query_dict)
    headers = bearer_auth_headers(token)
    resp = requests.post(full_url, headers=headers, data=json.dumps(data))
    resp_data = json.loads(resp.content)

    # read back the result
    if resp.status_code == requests.codes.ok:
        return resp_data
    raise ValueError('got an error loading: '+str(resp) +
                     '\n' + str(resp_data))

# eof
