import requests
import logging
import optparse
import sys

python_version = sys.version_info
assert python_version >= (3,5), 'This script requires Python >= 3.5. You appear to be running an older version of Python.'

# here the action options are set, among the other the default output file name alocation is set
usage = "USAGE: "
parser = optparse.OptionParser()
parser.add_option("-d", "--debug", action="store_true", dest="debug",
                  help="Enable debug messages in output. Sets the logging level to DEBUG.", default=False)
parser.add_option("-o", "--output-file", action="store", dest="outfile", default="./wikidata_countries.csv",
                  help="Store output in file.")
(options, args) = parser.parse_args()

# the logging level is set to debug (50) here
if options.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)

# these two snippets show the python version and outfile name on the cmd line
logging.debug("Python version: %s",python_version)
logging.debug("Output file %s" % options.outfile)

# this sets the sparql query used for data retrieval from wikidata
query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?country 
?ISO_3166_1_alpha_3_code 
?ISO_3166_1_alpha_2_code 
?countryLabel 
?altlabel 
?geonamesid 
?contains_administrative_territorial_entity 
?contains_administrative_territorial_entityLabel 
WHERE
{ SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
?country wdt:P31 wd:Q6256.
OPTIONAL { ?country wdt:P298 ?ISO_3166_1_alpha_3_code. }
OPTIONAL { ?country wdt:P297 ?ISO_3166_1_alpha_2_code. }
OPTIONAL { ?country wdt:P150 ?contains_administrative_territorial_entity. }
OPTIONAL { ?country skos:altLabel ?altlabel. }
OPTIONAL { ?country wdt:P1566 ?geonamesid. }
FILTER (lang(?altlabel) = 'en').
}'''

# set the url parameters for the wikidata API
# 'Accept' header ensures the query results in a csv format
url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
headers = {'Accept': 'text/csv', 'User-Agent': "user_agent"}
response = requests.get(url, headers=headers, params={'query': query})

# if the http status code is not 200, this snippet will return the status code so potential errors can be revised
if response.status_code != 200:
    logging.error('WikiData API Request failed with response code %s' % response.content)
    exit(1)

# this shows the debugging message for the response body and writes it to the outfile with the above defaulame and location
logging.debug(response.text)
with open(options.outfile, "w") as f:
    f.write(response.text)

