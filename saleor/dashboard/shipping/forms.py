from __future__ import unicode_literals

from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

from ...shipping.models import ShippingMethod, ShippingMethodCountry, ShippingCountry


class ShippingMethodForm(forms.ModelForm):

    class Meta:
        model = ShippingMethod
        exclude = []


ShippingMethodCountryFormSet = inlineformset_factory(
    ShippingMethod, ShippingMethodCountry, fields=['country_code', 'price'],
    can_delete=True, extra=2, min_num=1, validate_min=True)


class ShippingCountryForm(forms.ModelForm):

    class Meta:
        model = ShippingCountry
        exclude = []


class ShippingCitiesForm(forms.Form):

    file = forms.FileField()


class ShippingOfficesForm(forms.Form):

    file = forms.FileField()


def validate_file_extension(value):
    if value.file.content_type != 'application/x-yaml':
        raise ValidationError(u'Only YAML format is supported.')
