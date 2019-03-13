# DataFinnovation API Demos

Here are some basic Python 3.6 demos for the DataFinnovation API.
Authentication is done via OAuth2.
Basic wrappers to facilitate this are included as part of the demo
package and this code can run with the standard
libraries + requests.

To use any of these scripts set three environment variables:
* **DF_CLIENT_ID** to your client ID
* **DF_CLIENT_SECRET** to your API login secret
* **DF_API_KEY** to your API key

You can find these at https://webclient.dfnapp.com/.

## API Documentation
This API is documented at
https://app.swaggerhub.com/apis-docs/datafinnovation/clientapi/1.0/.

The simplest thing to do is work through these examples in the order
they are given.

## Searching For Facts
### [fact_search.py](fact_search.py)
This runs a query string query for facts.  It prints out
each hit.

### [fact_dsl_search.py](fact_dsl_search.py)
This runs a query for facts using the ElasticSearch DSL and prints
out the results.

### [fact_simple_search.py](fact_simple_search.py)
This runs a simple query string query for facts and prints out
each hit.

### [fact_form_search.py](fact_form_search.py)
This runs a fact search using the web-esque form interface.

## Searching For Documents
### [document_search.py](document_search.py)
This runs a query string query for document results.  It prints out
each result in turn, extracting the key and dumping the whole document
metadata dictionary.

### [document_dsl_query.py](document_dsl_query.py)
An example using the ES DSL interface.

### [document_form_search.py](document_form_search.py)
An example using the form interface.

## Loading Data By Reference
All those searches, both for documents and facts, contain a
"key" entry which identifies the referenced document.
If you know the document key you want - say from earlier search
work - then you can use this part of the API to pull information
directly.

### [document_field_names.py](document_field_names.py)
This loads all available field names for a given document key.
The example script contains a key - in practice you'll likely
pull a key from something like the document and fact searches
above.

### [document_field_values.py](document_field_values.py)
This pulls individual fact values from a document by key and
fact label.
The example script contains a key and some labels - in practice you'll
likely pull them from something like the document and fact searches above.

## Wrapper Code And Admin
### [oauth2_wrappers.py](oauth2_wrappers.py)
Some simple wrapper code to handle oauth2 matters.  This whole API
requires OAuth2 tokens.  

### [df_wrappers.py](df_wrappers.py)
Higher level wrappers for use in real-world examples.  These serve
to keep the demo code clean.

### [requirements.txt](requirements.txt)
Contains the basic dependencies for the demos to work.

### [requirements_more.txt](requirements_more.txt)
Contains a larger set of dependencies.  These are
not strictly required but have better error handling.  If you run into
trouble start by installing them.  Some of the "Real World Examples"
below also require additional packages.

## Real World Examples
We also include some non-toy cases.

### [oil_company_footnote_feed.py](oil_company_footnote_feed.py)
This generates a feed of interesting, recent, footnotes for a set of oil companies' US filings.  It employs the ES DSL facts search
interface.

### [indo_timeseries.py](indo_timeseries.py)
This pulls a timeseries for a single entry for an Indonesian
company.  It makes use of the documents string query search and
the non-search field & value interface.

### [count_filing_arrivals.py](count_filing_arrivals.py)
Count how many filings we have, by month, from the US SEC or
Japan EDINET.

### [bitcoin_occurrences.py](bitcoin_occurrences.py)
Count how many accounting entries have bitcoin in the name, and
how many unique companies have filed such entries.  Break down
totals by year.

### [korea_client_prospect.py](korea_client_prospect.py)
Finds the names of companies that have filed fields containing
given sets of words. This example focuses on derivative trading
client prospects -- but changing the keywords can easily
refocus the script.

### [footnote_sentiment_feed.py](footnote_sentiment_feed.py)
Grabs recent text footnotes from the US SEC and runs them through
a simple sentiment classifier.  Note this script requires two
additional dependencies:
[BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
and
[Vader Sentiment](https://github.com/cjhutto/vaderSentiment).
These are included in the requirements_more.txt file.

### [japan_filing_translate.py](japan_filing_translate.py)
Grabs a block of fields from Japanese filings and runs their
contents through [Google Translate](https://pypi.org/project/googletrans/).
This shows how seamlessly we feed UTF encoded text through the API.

### [trump_tax_cuts.py](trump_tax_cuts.py)
Finds records related to the Tax Cuts and Jobs Act of 2017 and
prints out (company name , field name) pairs that were filed.
These are all *ad hoc* non-standard non-GAAP fields.
