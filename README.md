# hseifert/NagoyaLookupService

The hseifert/NagoyaLookupService repository provides a web service based on an integrated database to extract Nagoya Protocol information from combined third party sources. It is a modular lookup service based on GPS coordinates to check indications on Nagoya requirements. Using latitude, longitude and a search radius the service checks possible nearby country borders that might need to be considered and more importantly whether these countries have signed the Nagoya Protocol or not.

#### How to cite
H. Seifert, A GIS - Enabled Lookup Service for Nagoya Protocol Indications, (2019), GitHub repository, https://github.com/hseifert/NagoyaLookupService

## Getting Started
To get a copy of this project on your local machine for development or testing purposes simply clone the repository using  

`git clone https://github.com/hseifert/NagoyaLookupService`

## Local usage

To start the service, move to the root directory containing the file called "local.yml".

Use `docker-compose -f local.yml build --no-cache` to build the three containers from scratch

Use `docker-compose -f local.yml up --force-recreate` to start and initialize the service.  
Once the debugger is active the API can be used to access the information from the containers (database).

#### Example

Use `http://localhost:8000/nagoya/gislookup/-5.825922,51.968407/` (exchange longitude,latitude with you own coordinates) to interact with the REST API 

Or

Use `http://localhost:8000/nagoya/lookup/`to go to the graphical user-friendly interface to make database queries using the form.

## Built With
[Django](https://www.djangoproject.com/) - The web framework used 

[Docker](https://www.docker.com/) - The container system used, Docker Toolbox for Windows , version 17.07.0 

[PostgreSQL](https://www.postgresql.org/) - The object-relational database system (version 2.0) used with a PostGIS extension (version 2.4)


## Versioning
We use [SemVer](https://semver.org/) for versioning. For the versions available, see the tags on this repository.

## Authors
* Hendrikje Seifert
* Ivaylo Kostadinov 
* Marc Weber 

## Licenses
This project is licensed under the MIT License - see the LICENSE.md file for details

#### Third party dependencies/requirements:

* Sphinx (BSD-3-clause) 
* django-extensions (MIT)
* Werkzeug (BSD-3-clause)
* django-test-plus (BSD-3-clause)
* factory-boy (MIT)
* django-debug-toolbar (BSD-3-clause)
* ipdb (BSD-3-clause)
* pytest-django (BSD-3-clause)
* pytest-sugar (BSD-3-clause)
* django-model-utils (BSD-3-clause)
* Pillow (PIL Software License)
* argon2-cffi (MIT)
* awesome-slugify (tbc)
* pytz (MIT)
* django-redis (BSD-3-clause)
* redis (BSD-3-clause)
* psycopg2 (LGPL)
* djangorestframework (BSD-3-clause)
* django-rest-swagger (BSD-3-clause)
* django-leaflet (LGPL)
* gevent (MIT)
* gunicorn (MIT)
* django-storages (BSD-3-clause)
* django-anymail (BSD-3-clause)
