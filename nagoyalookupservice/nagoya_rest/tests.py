from django.test import TestCase

from .forms import LookupForm


class TestForms(TestCase):

    def test_valid_lookup_form(self):
        data = {
            'latitude': -2.978,
            'longitude': 78.09,
            'radius': 5000,
        }
        form = LookupForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_values(self):
        data = {
            'latitude': -91.345,
            'longitude': 270.9,
            'radius': 'abcd',
        }
        form = LookupForm(data)
        self.assertFalse(form.is_valid())
        self.assertListEqual(
            [['Invalid latitude: -91.345'], ['Enter a whole number.'],
             ['Invalid longitude: 270.9']],
            list(form.errors.values())
        )
