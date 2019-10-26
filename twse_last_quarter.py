"""counts the number of filings for each month going back years"""

import calendar
import datetime

from oauth2_wrappers import gen_token
from df_wrappers import documents_stringquery

def prev_quarter_boundaries(now):
    """"return the start and end dates for the previous quarter"""
    first_of_month = datetime.datetime(now.year, now.month, 1)

    # 75 days before the 1st is always in the previous quarter
    date_in_prev_q = first_of_month - datetime.timedelta(days=75)

    q_y = date_in_prev_q.year
    q_start_m = int((date_in_prev_q.month-1) / 3)*3 + 1
    q_end_m = q_start_m + 2
    q_end_d = calendar.monthrange(q_y, q_end_m)[1]

    s_d = datetime.datetime(q_y, q_start_m, 1)
    e_d = datetime.datetime(q_y, q_end_m, q_end_d)

    return s_d, e_d

def main():
    """example code lives in one function"""

    # generate a token, we will be sending several queries off
    token = gen_token()
    # build the query string
    s_d, e_d = prev_quarter_boundaries(datetime.datetime.utcnow())
    s_str = s_d.strftime("%Y-%m-%d")
    e_str = e_d.strftime("%Y-%m-%d")
    query_str = (
        'filingsource:"Taiwan TWSE" AND ' +
        'enddate:[' + s_str + ' TO ' +
        e_str + ']'
    )
    # pull docs
    docs_res = documents_stringquery(query_str, False, token=token)
    # read out number of hits
    num_filings = docs_res['totalHits']
    # print it out
    print('Filing count from last quarter: ' + str(num_filings))

main()

# eof
