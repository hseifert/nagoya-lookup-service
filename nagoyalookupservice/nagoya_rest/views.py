import collections
import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from tzlocal import get_localzone

from .forms import LookupForm
from .models import GisLookup
from .serializers import LookupSerializer


# view for the JSON-based REST API
class LookupViewSet(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, longitude, latitude, radius):
        if not radius:
            radius = '5000'
        else:
            pass

        parties = GisLookup.objects.raw(
            "SELECT * from nplookup('{0} {1}'::varchar, {2});"
            "".format(longitude, latitude, radius))

        # validation check for lon and lat
        if (int(float(longitude)) not in range(-180, 180) and int(
                float(latitude)) not in range(-90, 90)):
            return HttpResponse(

                'Error 400: Bad request - Both input longitude and input latitude are out of their respective ranges. Please review.')

        else:
            pass
        if int(float(longitude)) not in range(-180, 180):
            return HttpResponse(
                'Error 400: Bad request - Input longitude is out of the respective range (-180 to 180). Please review.')
        elif int(float(latitude)) not in range(-90, 90):
            return HttpResponse(
                'Error 400: Bad request - Input latitude is out of the respective range (-90 to 90). Please review.')
        else:
            pass

        serialized_data = LookupSerializer(parties, many=True)

        a = {
            'disclaimer': "This lookup service is provided as an information service only and does not constitute legal advice. While it is set up to provide the latest Nagoya \
                            party information, this service relies on third party data sources. This is particularly \
                            true with regard to the information and documents on each individual country's national law which this database does not comprehensively cover. \
                            This service additionally contains links to external websites and content originating from third parties. Such external links are not investigated, monitored or checked for \
                            accuracy, validity, reliability, availability and completeness by us. Your use of this service and your reliance on any kind of information provided here is solely at your own risk.",
            'query_details': {
                'database_last_updated:': settings.DB_TIMESTAMP,
                'query_date_time:': datetime.datetime.now(
                    get_localzone()).strftime("%Y-%m-%dT%H:%M:%S"),
                'longitude': longitude,
                'latitude': latitude,
                'radius': {
                    'value': radius,
                    'unit': "m"
                },
                'un_url': "https://treaties.un.org/pages/ViewDetails.aspx?src=IND&mtdsg_no=XXVII-8-b&chapter=27&clang=_en"
            },
            'results': serialized_data.data
        }

        ordered_a = collections.OrderedDict()
        ordered_a['disclaimer'] = a['disclaimer']
        ordered_a['query_details'] = a['query_details']
        ordered_a['results'] = a['results']

        return Response(ordered_a)


# view for the HTML-based interface with forms
class WebLookup(View):
    def get(self, request):
        longitude = request.GET.get('longitude', None)
        latitude = request.GET.get('latitude', None)
        radius = request.GET.get('radius', 5000)

        if longitude is None:
            form = LookupForm()
            return render(request, 'lookup.html', {'empty': True, 'form': form})
        else:
            form = LookupForm({'longitude': longitude, 'latitude': latitude,
                               'radius': radius})
            if form.is_valid():
                print('VALID')
                parties = GisLookup.objects.raw(
                    "SELECT * from nplookup('{0} {1}'::varchar, {2});".format(
                        form.cleaned_data['longitude'],
                        form.cleaned_data['latitude'],
                        form.cleaned_data['radius']))

                return render(request, 'lookup.html',
                              {'parties': parties, 'form': form,
                               'latitude': form.cleaned_data['latitude'],
                               'longitude': form.cleaned_data['longitude'],
                               'radius': form.cleaned_data['radius'],
                               'database_last_updated': settings.DB_TIMESTAMP,
                               'query_date_time': datetime.datetime.now(
                                   get_localzone()).strftime(
                                   "%Y-%m-%dT%H:%M:%S")})


            else:
                return render(request, 'lookup.html',
                              {'form': form, 'latitude': latitude,
                               'longitude': longitude, 'radius': radius})



# view for the HTML-based list of the data sources
class DataSources(View):
    def get(self, request):
        return render(request, 'datasources.html',
                      {'database_last_updated': settings.DB_TIMESTAMP})
