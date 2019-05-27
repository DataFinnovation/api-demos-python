"""
This script pulls all press releases (8-Ks) for a given CIK in
a given date range and returns the average sentiment of the text.
NOTE: this requires beautifulsoup4 and vaderSentiment
"""

import statistics

import bs4
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from df_wrappers import facts_stringquery

def main():
    """example code main function"""

    query_string = '''
        filingsource:"US SEC Non-XBRL" AND filerid:1065280 AND
        enddate:[2018-01-01 TO 2018-12-31] AND reporttype:"8-K"
    '''

    # send off the query
    resp_data = facts_stringquery(query_string, False)
    # keep unique list of company names from results

    scores = []
    # set up a vader sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # for each hit
    for ele in resp_data['hits']:
        # clean up the html and put it in simple text
        soup = bs4.BeautifulSoup(ele['source']['fieldvalue'], 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        as_text = soup.get_text().strip()

        # score the text
        vader_score = analyzer.polarity_scores(as_text)
        # and record the whole entry alongside the score
        scores.append(vader_score['compound'])

    average_score = statistics.mean(scores)
    print(average_score)

main()

# eof
