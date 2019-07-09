from django import forms
from django.utils.translation import gettext_lazy as _


class Latitude(forms.FloatField):
    def validate(self, value):
        super(forms.FloatField, self).validate(value)
        if (value < -90) or (value > 90):
            raise forms.ValidationError(
                _('Invalid latitude: %(value)s'),
                code='invalid',
                params={'value': value},
            )


class Longitude(forms.FloatField):
    def validate(self, value):
        super(forms.FloatField, self).validate(value)
        if (value < -180) or (value > 180):
            raise forms.ValidationError(
                _('Invalid longitude: %(value)s'),
                code='invalid',
                params={'value': value},
            )


class LookupForm(forms.Form):
    latitude = Latitude()
    longitude = Longitude()
    radius = forms.IntegerField()
