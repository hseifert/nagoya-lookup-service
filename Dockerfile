FROM mdillon/postgis:10

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip curl && \
    rm -r /var/lib/apt/lists/* && \
    pip3 install certifi requests



COPY sql/createnagoyatable.sql /docker-entrypoint-initdb.d/
COPY sql/creategeonamestable.sql /docker-entrypoint-initdb.d/
COPY sql/createwikidatatable.sql /docker-entrypoint-initdb.d/
COPY sql/fillandalternagoyatable.sql /docker-entrypoint-initdb.d/
COPY sql/coordinatefunction.sql /docker-entrypoint-initdb.d/nplookup.sql
COPY sql/fillandaltergeonamestable.sql /docker-entrypoint-initdb.d/
COPY sql/fillwikidatatable.sql /docker-entrypoint-initdb.d/
COPY sql/updateeezlanduniontable.sql /docker-entrypoint-initdb.d/
RUN mv /docker-entrypoint-initdb.d/postgis.sh /docker-entrypoint-initdb.d/apostgis.sh

#Import GIS data
COPY thirdpartydata/EEZ_land_v2_201410.shp /
COPY thirdpartydata/EEZ_land_v2_201410.shx /
COPY thirdpartydata/EEZ_land_v2_201410.dbf /

RUN shp2pgsql -s 4326 /EEZ_land_v2_201410.shp public.eezlandunion > /docker-entrypoint-initdb.d/eezlandunion.sql

#Download geonames data (i.e. country info file)
RUN curl -SL http://download.geonames.org/export/dump/countryInfo.txt | grep -v -E '^#' > /countryInfo.txt
#Download nagoya country info
COPY pyscripts/fetch-nagoya-info.py /
RUN python3 /fetch-nagoya-info.py -o /nagoya_countries.csv

COPY pyscripts/fetch-wikidata.py /
RUN python3 /fetch-wikidata.py -o /wikidata_countries.csv



RUN echo "I am alive!"
