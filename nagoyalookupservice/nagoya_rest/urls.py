from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

from . import views

schema_view = get_swagger_view(
    title='Nagoya Lookup API Documentation',
    patterns=[
        url(
            regex=r'^/nagoya/gislookup/(?P<longitude>(\-?\d+(\.\d+)?)),(?P<latitude>(\-?\d+(\.\d+)?)),?(?P<radius>([0-9]*))/$',
            view=views.LookupViewSet.as_view(),
            name='nagoya_gislookup')], )

urlpatterns = [
    url(
        regex=r'^lookup/doc$',
        view=schema_view,
        name='swagger'
    ),
    url(
        regex=r'^gislookup/(?P<longitude>(\-?\d+(\.\d+)?)),(?P<latitude>(\-?\d+(\.\d+)?)),?(?P<radius>([0-9]*))/$',
        view=views.LookupViewSet.as_view(),
        name='nagoya_gislookup'
    ),
    url(
        regex=r'^lookup/$',
        view=views.WebLookup.as_view(),
        name='web-lookup',
    ),
    url(
        regex=r'^lookup/datasources/$',
        view=views.DataSources.as_view(),
        name='datasources',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
