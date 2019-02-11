"""
pull recent accounting-related footnotes and
compute sentiment scores
NOTE: this requires beautifulsoup4 and vaderSentiment
"""

import datetime

import bs4
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from df_wrappers import facts_dslquery

# how many days back to go for filings
NUM_DAYS = 3

# display the top N most positive and negative footnotes
NUM_DISPLAY = 3

# footnotes under then length will be skipped
MIN_TEXT_LENGTH = 30

# the max number of footnotes to process
MAX_FOOTNOTE_NUMBER = 500

def score_sort_cmp(es_hit):
    """comparator for sorting by sentiment"""
    return es_hit['vader_score']['compound']

def main():
    """example code main function"""

    # first set up a nice date range
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(days=NUM_DAYS)

    # format boundary dates
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S')
    end_str = now.strftime('%Y-%m-%dT%H:%M:%S')

    # query params
    params = {'maxresult' : MAX_FOOTNOTE_NUMBER}
    # grab recent entries from the us
    # that are non-numeric and not from the "rr" taxonomy
    dsl_dict = {
        "query": {
            "constant_score" : {
                "filter" : {
                    "bool" : {
                        "must" : [
                            # fields that include accouting in their name
                            {"term" : {"fieldname" : "accounting"}},
                            # from the appropriate date range
                            {"range" : {"retrievaltime" : {"gte" : start_str,
                                                           "lt" : end_str}}},
                            # from the us sec
                            {"terms" : {"filingsource" : ["US SEC"]}},
                        ],
                        "must_not" : [
                            # without units means non-numeric
                            {"exists" : {"field" : "units"}},
                            # the rr taxonomy contains mostly boilerplate text
                            {"term" : {"fieldtag": "rr:"}}
                        ]
                    }
                }
            }
        }
    }

    # send off the query
    resp_data = facts_dslquery(dsl_dict, params=params)
    # keep unique list of company names from results

    scored_entries = []
    # set up a vader sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # for each hit
    for ele in resp_data['hits']:
        # clean up the html and put it in simple text
        soup = bs4.BeautifulSoup(ele['source']['fieldvalue'], 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        as_text = soup.get_text().strip()
        if len(as_text) < MIN_TEXT_LENGTH:
            # skip short messages
            continue

        # score the text
        vader_score = analyzer.polarity_scores(as_text)
        # and record the whole entry alongside the score
        scored_entries.append({'record' : ele,
                               'vader_score' : vader_score,
                               'as_text' : as_text})

    # sort by compound sentiment score
    scored_entries.sort(key=score_sort_cmp, reverse=True)

    # and print out the top and bottom scores
    for i in range(0, NUM_DISPLAY):
        print('---')
        print('+ve entry: '+str(scored_entries[i]['record']))
        print('as text: '+scored_entries[i]['as_text'])
        print('score: '+str(scored_entries[i]['vader_score']['compound']))
        print('---')
        print('-ve entry: '+str(scored_entries[-(i+1)]['record']))
        print('as text: '+scored_entries[-(i+1)]['as_text'])
        print('score: '+str(scored_entries[-(i+1)]['vader_score']['compound']))
        print('---')

main()

# eof
