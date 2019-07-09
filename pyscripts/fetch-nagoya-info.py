import csv
import json
import logging
import optparse
import sys
import urllib.request


python_version = sys.version_info
assert python_version >= (3,5), 'This script requires Python >= 3.5. You appear to be running an older version of Python.'


usage = "USAGE: "
parser = optparse.OptionParser()
parser.add_option("-d", "--debug", action="store_true", dest="debug",
                  help="Enable debug messages in output. Sets the logging level to DEBUG.", default=False)
parser.add_option("-o", "--output-file", action="store", dest="outfile",
                  help="Store output in file.")
(options, args) = parser.parse_args()

# SET logging LEVEL
if options.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)

logging.debug("Python version: %s",python_version)


if not options.outfile:
    outfile = "./nagoya_countries.csv"
else:
    outfile = options.outfile

abs_api = "https://api.cbd.int/api/v2013/countries"
nagoya_treaty_code = "XXVII8b"

with urllib.request.urlopen(abs_api) as resource:
    response_code = resource.getcode()
    logging.debug("Request response code:"+str(response_code))
    if response_code != 200:
        logging.error("Request returned HTTP response: "+str(response_code))
    else:
        json_data = json.loads(resource.read().decode())

nagoya_countries = []

for country in json_data:
    nagoya_treaty = country['treaties'][nagoya_treaty_code]
    nagoya_details = [country['code'],nagoya_treaty['party'],nagoya_treaty['instrument'],nagoya_treaty['deposit'],nagoya_treaty['signature']]
    nagoya_countries.append(nagoya_details)

with open(outfile, 'w+') as output:
    writer = csv.writer(output, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
    writer.writerow(['code', 'party', 'instrument', 'deposit', 'signature'])
    writer.writerows(nagoya_countries)