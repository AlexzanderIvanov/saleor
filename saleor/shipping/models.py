from __future__ import absolute_import

from itertools import groupby
from operator import itemgetter

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import pgettext_lazy, gettext as _
from django_prices.models import PriceField
from prices import PriceRange


@python_2_unicode_compatible
class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    @property
    def countries(self):
        countries = [str(country) for country in self.price_per_country.all()]
        return countries

    @property
    def price_range(self):
        prices = list(self.price_per_country.values_list('price', flat=True))
        if prices:
            return PriceRange(min(prices), max(prices))


class ShippingMethodCountryQueryset(models.QuerySet):
    def unique_for_country_code(self, country_code):
        shipping = self.filter(
            Q(country_code=country_code) |
            Q(country_code=ShippingMethodCountry.ANY_COUNTRY))
        shipping = shipping.order_by('shipping_method_id')
        shipping = shipping.values_list('shipping_method_id', 'id', 'country_code')
        grouped_shipping = groupby(shipping, itemgetter(0))
        any_country = ShippingMethodCountry.ANY_COUNTRY

        ids = []

        for shipping_method_id, method_values in grouped_shipping:
            method_values = list(method_values)
            # if there is any country choice and specific one remove any country choice
            if len(method_values) == 2:
                method = [val for val in method_values if val[2] != any_country][0]
            else:
                method = method_values[0]
            ids.append(method[1])
        return self.filter(id__in=ids)


@python_2_unicode_compatible
class ShippingMethodCountry(models.Model):
    ANY_COUNTRY = ''
    COUNTRIES = {
        ("BG", "Bulgaria"),
    }
    COUNTRY_CODE_CHOICES = [(ANY_COUNTRY, _('Any country'))] + list(COUNTRIES)

    country_code = models.CharField(
        choices=COUNTRY_CODE_CHOICES, max_length=2, blank=True, default=ANY_COUNTRY)
    price = PriceField(
        pgettext_lazy('Shipping method region field', 'price'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2)
    shipping_method = models.ForeignKey(ShippingMethod, related_name='price_per_country')

    objects = ShippingMethodCountryQueryset.as_manager()
    country = models.Manager()

    class Meta:
        unique_together = ('country_code', 'shipping_method')

    def __str__(self):
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.get_FOO_display  # noqa
        return "%s %s" % (self.shipping_method, self.get_country_code_display())

    def get_total(self):
        return self.price


@python_2_unicode_compatible
class ShippingCountry(models.Model):
    ANY_COUNTRY = ''
    COUNTRIES = {
        ("BG", "Bulgaria"),
    }
    COUNTRY_CODE_CHOICES = [(ANY_COUNTRY, _('Any country'))] + list(COUNTRIES)

    country_code = models.CharField(
        choices=COUNTRY_CODE_CHOICES, max_length=2, blank=True, default=ANY_COUNTRY, unique=True)

    def __str__(self):
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.get_FOO_display  # noqa
        return "%s %s" % (self.country_code, self.get_country_code_display())


@python_2_unicode_compatible
class ShippingCity(models.Model):
    """Example yaml format containit city data
    - hub_code: '4000'
        hub_name: "\u041F\u043B\u043E\u0432\u0434\u0438\u0432"
        hub_name_en: Plovdiv
          id: '61186'
          id_country: '1033'
          id_office: '37'
          id_zone: '1'
          name: Aksakovo
          name_en: Aksakovo
          post_code: '9602'
          region: ''
          region_en: ''
          type: "\u0433\u0440."
          updated_time: '2016-01-01 03:00:10'"""
    external_id = models.IntegerField(primary_key=True)
    country = models.ForeignKey(ShippingCountry)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    region_en = models.CharField(max_length=255)
    village_or_city = models.CharField(max_length=2)
    update_time = models.DateTimeField(max_length=255)


@python_2_unicode_compatible
class ShippingOffice(models.Model):
    """Example yaml format containit city data
    -     address: "Варна кв. Център ул. Цариброд №48"
          address_en: "Varna kv. Center ul. Tsaribrod \u211648"
          city_name: "Варна"
          city_name_en: Varna
          id: '569'
          id_city: '7'
          name: "Варна ЖП Гаар"
          name_en: Varna JP gara
          office_code: '9006'
          phone: +359 87 9922026,+359 52 610619
          post_code: '9000'
          updated_time: '2016-04-14 12:09:40'"""
    external_id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=255)
    address_en = models.CharField(max_length=255)
    country = models.ForeignKey(ShippingCountry)
    city = models.ForeignKey(ShippingCity)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    office_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)
    update_time = models.DateTimeField(max_length=255, )
