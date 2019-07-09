from django.db import models


# model for the JSON-based REST API and the HTML-based service interface
class GisLookup(models.Model):
    nagoya_iso2 = models.CharField(primary_key=True)
    party_date = models.DateField()
    marine_regions_country = models.CharField()
    wikidata_country = models.CharField()
    distance = models.IntegerField()

    # defining the unique key for the data
    def natural_key(self):
        return self.iso_2_code

    # appending the iso2 code to the CBD url to get to the country profile, when null then return n/a
    def _get_cbd_profile(self):
        if not self.nagoya_iso2:
            return 'n/a'
        else:
            return 'https://www.cbd.int/countries/?country={0}'.format(
                self.nagoya_iso2)

    cbd_profile = _get_cbd_profile

    # appending the iso2 code to the ABSCH url to get to the country profile, when null then return n/a
    def _get_absch_profile(self):
        if not self.nagoya_iso2:
            return 'n/a'
        else:
            return 'https://absch.cbd.int/countries/{0}'.format(
                self.nagoya_iso2)

    absch_profile = _get_absch_profile

    class Meta:
        app_label = 'nagoya'
        db_table = 'nagoya'
        managed = False
