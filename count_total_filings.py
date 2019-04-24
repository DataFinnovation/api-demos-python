""" A simple script to count total available filings by source. """

from df_wrappers import documents_dslquery

def main():
    """
    no args
    """

    # A list of sources we care about.
    source_name_list = ['US SEC', 'UK CH', 'Chile SVS',
                        'Peru SMV', 'Japan EDINET', 'Taiwan TWSE',
                        'Indonesia IDX', 'Spain CNMV', 'Korea FSS',
                        'India BSE', 'US SEC Non-XBRL']

    # We do not need any results, just the count.
    params = {'maxresult' : 1}
    for source_name in source_name_list:
        # Build a simple query.
        dsl_query = {
            "query": {
                "term" : {
                    "filingsource": source_name
                }
            }
        }

        # Post the request.
        resp_data = documents_dslquery(dsl_query, params=params)
        # Extract the hit count.
        filing_count = resp_data['totalHits']
        # And print the result, sensibly formtted.
        print(source_name + ' : ' + "{:,}".format(filing_count))

if __name__ == '__main__':
    main()

# eof
