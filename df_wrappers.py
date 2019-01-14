"""
API Wrapper Functions
This operates at a higher level than oauth2_wrappers and is intended
for substantive examples.
"""

import oauth2_wrappers

def prep_token(**kwargs):
    """helper to build a token if needed, avoid excessive token generation"""
    token = kwargs.get('token')
    if not token:
        token = oauth2_wrappers.gen_token()
    return token

def facts_dslquery(dsl_dict, **kwargs):
    """Sends off a facts dslquery"""
    token = prep_token(**kwargs)
    api_url = 'facts/dslquery'
    param_dict = kwargs.get('params', {})
    post_dict = {'dslquery' : dsl_dict}
    resp_data = oauth2_wrappers.df_post(api_url, token, post_dict, param_dict)
    return resp_data

def documents_dslquery(dsl_dict, **kwargs):
    """Sends off a facts dslquery"""
    token = prep_token(**kwargs)
    api_url = 'documents/dslquery'
    param_dict = kwargs.get('params', {})
    post_dict = {'dslquery' : dsl_dict}
    resp_data = oauth2_wrappers.df_post(api_url, token, post_dict, param_dict)
    return resp_data

def documents_stringquery(querystring, simplequery, **kwargs):
    """Sends off a string query for documents"""
    token = prep_token(**kwargs)
    query_dict = {'querystring':querystring,
                  'simplequery':simplequery}
    if 'sortfield' in kwargs:
        query_dict['sortfield'] = kwargs['sortfield']
    if 'sortascending' in kwargs:
        query_dict['sortascending'] = kwargs['sortascending']
    api_url = 'documents/textquery'
    resp_data = oauth2_wrappers.df_get(api_url, token, query_dict)
    return resp_data

def document_field_values(doc_key, field_names, **kwargs):
    """Sends off a field value query for a document"""
    token = prep_token(**kwargs)
    fields_url = 'docfields'
    post_dict = {'documentKey' : doc_key,
                 'fieldNames': field_names}
    resp_data = oauth2_wrappers.df_post(fields_url, token, post_dict, {})
    return resp_data

# eof
