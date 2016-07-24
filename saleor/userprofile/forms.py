# encoding: utf-8
from __future__ import unicode_literals

from collections import defaultdict

from django import forms
from django.utils.translation import ugettext as _
from i18naddress import validate_areas

from .models import Address
from saleor.shipping.models import ShippingCity, ShippingOffice


class AddressForm(forms.ModelForm):

    AUTOCOMPLETE_MAPPING = (
        ('first_name', 'given-name'),
        ('last_name', 'family-name'),
        ('company_name', 'organization'),
        ('street_address_1', 'address-line1'),
        ('street_address_2', 'address-line2'),
        ('city', 'address-level2'),
        ('postal_code', 'postal-code'),
        ('country_area', 'address-level1'),
        ('city_area', 'address-level3'),
        ('phone', 'tel'),
        ('email', 'email'),
        ('office', 'office')
    )

    class Meta:
        model = Address
        exclude = ['country']

    def __init__(self, *args, **kwargs):
        autocomplete_type = kwargs.pop('autocomplete_type', None)
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['city'].label_from_instance = lambda obj: "%s" % obj.name

        self.fields['office'].label_from_instance = lambda obj: "%s" % obj.name

        if hasattr(self.instance, 'city'):
            self.fields['office'].queryset = ShippingOffice.objects.filter(city=self.instance.city)

        autocomplete_dict = defaultdict(
            lambda: 'off', self.AUTOCOMPLETE_MAPPING)
        for field_name, field in self.fields.items():
            if autocomplete_type:
                autocomplete = '%s %s' % (
                    autocomplete_type, autocomplete_dict[field_name])
            else:
                autocomplete = autocomplete_dict[field_name]
            field.widget.attrs['autocomplete'] = autocomplete

    def clean(self):
        clean_data = super(AddressForm, self).clean()
        if 'city' in clean_data:
            self.fields['office'].queryset = ShippingOffice.objects.filter(city=clean_data.get('city'))
            self.validate_areas(
                clean_data.get('city'), clean_data.get('city_area'),
                clean_data.get('postal_code'), clean_data.get('street_address_1'),
                clean_data.get('office'), clean_data.get('to_office'))
        return clean_data

    def validate_areas(self,
                       city, city_area, postal_code, street_address, office, to_office):
        error_messages = defaultdict(
            lambda: _('Invalid value'), self.fields['city'].error_messages)
        errors, validation_data = validate_areas(
            str(self.instance.country), None, city.name,
            city_area, postal_code, street_address)

        # if 'country' in errors:
        #     self.add_error('country', _(
        #         '%s is not supported country code.') % self.instance.country)
        if 'street_address' in errors:
            error = error_messages[errors['street_address']] % {
                'value': street_address}
            self.add_error('street_address_1', error)
        if 'city' in errors and errors['city'] == 'required':
            error = error_messages[errors['city']] % {
                'value': city}
            self.add_error('city', error)
        if 'city_area' in errors and errors['city_area'] == 'required':
            error = error_messages[errors['city_area']] % {
                'value': city_area}
            self.add_error('city_area', error)
        if 'postal_code' in errors:
            if errors['postal_code'] == 'invalid':
                example = validation_data.postal_code_example
                if example:
                    example = example.replace(',', ', ')
                    error = _(
                        'Invalid postal code. Please follow the format: %(example)s') % {
                            'example': example}
                else:
                    error = _('Invalid postal code.')
            else:
                error = error_messages[errors['postal_code']] % {
                    'value': postal_code}
            self.add_error('postal_code', error)
        if to_office and not office:
            self.add_error('office', 'Invalid office')
        elif not to_office and not street_address:
            self.add_error('street_address_1', 'Invalid address')


