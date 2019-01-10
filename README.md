# DataFinnovation API Demos

Here are some basic Python 3.6 demos for the DataFinnovation API.
Authentication is done via OAuth2.
Basic wrappers to facilitate this are included as part of the demo
package and this code can run with the standard
libraries + requests.

To use any of these scripts set two environment variables:
* **DF_CLIENT_ID** to your client ID
* **DF_CLIENT_SECRET** to your API login secret

You can generate these for your web application at
https://webclient.dfnapp.com/.

## API Documentation
This API is documented at https://clientapi.dfnapp.com/swagger-ui.html#/.

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

### [requirements.txt](requirements.txt)
Contains the basic dependencies for the demos to work

### [requirements_more.txt](requirements_more.txt)
Contains a larger set of dependencies.  These are
not strictly required but have better error handling.  If you run into
trouble start by installing them.

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
