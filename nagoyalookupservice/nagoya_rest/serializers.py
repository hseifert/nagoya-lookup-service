from rest_framework import serializers
from .models import GisLookup


# serializing the model data
class LookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GisLookup
        fields = ('nagoya_iso2', 'party_date', 'marine_regions_country',
                  'wikidata_country', 'distance', 'absch_profile',
                  'cbd_profile')
