"""
pull total assets and gross non performing assets for
indian banks, compute a simple ratio, and dump results
in csv format.
"""

from locale import atof, setlocale, LC_ALL

from df_wrappers import facts_stringquery
from df_wrappers import documents_dslquery

# query params
MAX_FACT_NUMBER = 5000
QUERY_PARAMS = {'maxresult' : MAX_FACT_NUMBER}

def get_company_names():
    """helper to get company names and ids"""
    dsl_dict = {
        "query": {
            "constant_score" : {
                "filter" : {
                    "bool" : {
                        "must" : [
                            {"term" : {"companyname" : "bank"}},
                            {"term" : {"filingsource" : "India BSE"}},
                        ]}}}}}
    # send off the query
    resp_data = documents_dslquery(dsl_dict, params=QUERY_PARAMS)

    # list of all names
    company_names = {hit['source']['companyname'] for hit in resp_data['hits']}
    filerids = {}
    for hit in resp_data['hits']:
        filerids[hit['source']['companyname']] = hit['source']['filerid']
    return company_names, filerids

def main():
    """example code main function"""

    # results are in utf8, this makes atof work smoothly
    setlocale(LC_ALL, 'en_US.UTF-8')
    company_names, filerids = get_company_names()

    # and data structures
    assets = {}
    npassets = {}
    for name in company_names:
        assets[name] = {}
        npassets[name] = {}

    for name in company_names:
        filerid = filerids[name]
        # pull in revenue-related entries
        query_string = (
            'filingsource:"India BSE" AND filerid:"' +
            filerid + '" AND fieldname:assets'
        )

        # send off the query
        resp_data = facts_stringquery(query_string, False, maxresult=MAX_FACT_NUMBER)

        for ele in resp_data['hits']:
            fieldtag = ele['source']['fieldtag']
            enddate = ele['source']['enddate']
            fieldvalue = ele['source']['fieldvalue']
            if fieldtag == 'in-bse-fin:Assets':
                # find the total assets tag
                if enddate in assets[name]:
                    assets[name][enddate] = max(assets[name][enddate],
                                                atof(fieldvalue))
                else:
                    assets[name][enddate] = atof(fieldvalue)
            elif fieldtag == 'in-bse-fin:GrossNonPerformingAssets':
                # and the gross npa tag
                if enddate in npassets[name]:
                    npassets[name][enddate] = max(npassets[name][enddate],
                                                  atof(fieldvalue))
                else:
                    npassets[name][enddate] = atof(fieldvalue)

    # and print out a well-formatted version of the results
    print(','.join(['bank name,date,non-performing assets as % of total assets',
                    'total assets', 'np assets']))
    for name in company_names:
        for date in assets[name]:
            if date in npassets[name]:
                # so this date is in both
                tot_assets = assets[name][date]
                npa = npassets[name][date]
                print(','.join([name, date, str(100.0*npa/tot_assets)+'%',
                                str(tot_assets), str(npa)]))

main()

# eof
