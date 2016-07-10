from __future__ import unicode_literals

import dateutil.parser
import yaml
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .forms import ShippingMethodForm, ShippingMethodCountryFormSet, ShippingCountryForm, ShippingCitiesForm, \
    ShippingOfficesForm
from ...core.utils import get_paginator_items
from ...shipping.models import ShippingCity, ShippingCountry, ShippingMethod, ShippingOffice


@staff_member_required
def shipping_method_list(request):
    methods = ShippingMethod.objects.prefetch_related('price_per_country').all()
    methods = get_paginator_items(methods, 30, request.GET.get('page'))
    ctx = {'shipping_methods': methods}
    return TemplateResponse(request, 'dashboard/shipping/method_list.html', ctx)


@staff_member_required
def shipping_countries_list(request):
    countries = ShippingCountry.objects.all()
    countries = get_paginator_items(countries, 30, request.GET.get('page'))
    ctx = {'shipping_countries': countries}
    return TemplateResponse(request, 'dashboard/shipping/countries_list.html', ctx)


@staff_member_required
def shipping_cities_list(request):
    cities = ShippingCity.objects.filter(country__country_code="BG")
    cities = get_paginator_items(cities, 30, request.GET.get('page'))
    ctx = {'shipping_cities': cities}
    return TemplateResponse(request, 'dashboard/shipping/cities_list.html', ctx)


@staff_member_required
def shipping_offices_list(request):
    offices = ShippingOffice.objects.filter(country__country_code="BG").order_by('city')
    offices = get_paginator_items(offices, 30, request.GET.get('page'))
    ctx = {'shipping_offices': offices}
    return TemplateResponse(request, 'dashboard/shipping/offices_list.html', ctx)


@staff_member_required
def shipping_method_edit(request, method):
    form = ShippingMethodForm(request.POST or None, instance=method)
    formset = ShippingMethodCountryFormSet(request.POST or None, instance=method)
    if form.is_valid() and formset.is_valid():
        method = form.save()
        formset.save()
        msg = _('%s method saved') % method
        messages.success(request, msg)
        return redirect('dashboard:shipping-methods')
    ctx = {'shipping_method_form': form,
           'price_per_country_formset': formset, 'shipping_method': method}
    return TemplateResponse(request, 'dashboard/shipping/method_form.html', ctx)


@staff_member_required
def shipping_method_add(request):
    method = ShippingMethod()
    return shipping_method_edit(request, method)


def shipping_country_edit(request, country):
    form = ShippingCountryForm(request.POST or None, instance=country)
    if form.is_valid():
        country = form.save()
        msg = _('%s method saved') % country
        messages.success(request, msg)
        return redirect('dashboard:countries-list')
    ctx = {'shipping_country_form': form, 'shipping_country': country}
    return TemplateResponse(request, 'dashboard/shipping/country_form.html', ctx)


@staff_member_required
def shipping_country_add(request):
    country = ShippingCountry()
    return shipping_country_edit(request, country)


@staff_member_required
def shipping_cities_load(request):
    form = ShippingCitiesForm(request.POST, request.FILES)
    if form.is_valid():
        __store_cities_in_db(request.FILES['file'])
        msg = _('%s method saved') % 'cities'
        messages.success(request, msg)
        return redirect('dashboard:shipping-cities-list')
    ctx = {'shipping_cities_form': form,}
    return TemplateResponse(request, 'dashboard/shipping/cities_form.html', ctx)


def __store_cities_in_db(f):
    cities_data = yaml.safe_load(f)

    country = ShippingCountry.objects.get(country_code="BG")

    for city_data in cities_data:
        updated_date = dateutil.parser.parse(city_data['updated_time'])
        updated_date = timezone.make_aware(updated_date, timezone.get_current_timezone())
        city = ShippingCity(external_id=city_data['id'],
                            country=country,
                            name=city_data['name'],
                            name_en=city_data['name_en'],
                            post_code=city_data['post_code'],
                            region=city_data['region'],
                            region_en=city_data['region_en'],
                            village_or_city=city_data['type'],
                            update_time=updated_date)
        city.save()


@staff_member_required
def shipping_offices_load(request):
    form = ShippingOfficesForm(request.POST, request.FILES)
    if form.is_valid():
        __store_offices_in_db(request.FILES['file'])
        msg = _('%s method saved') % 'offices'
        messages.success(request, msg)
        return redirect('dashboard:shipping-offices-list')
    ctx = {'shipping_offices_form': form,}
    return TemplateResponse(request, 'dashboard/shipping/offices_form.html', ctx)


def __store_offices_in_db(f):
    offices_data = yaml.safe_load(f)

    country = ShippingCountry.objects.get(country_code="BG")
    cities = __get_cities_dictionary()

    for office in offices_data:
        city = cities.get(int(office['id_city']))
        if city:
            updated_date = dateutil.parser.parse(office['updated_time'])
            updated_date = timezone.make_aware(updated_date, timezone.get_current_timezone())
            office = ShippingOffice(address=office['address'],
                                    address_en=office['address_en'],
                                    external_id=office['id'],
                                    city=city,
                                    country=country,
                                    name=office['name'],
                                    name_en=office['name_en'],
                                    office_code=office['office_code'],
                                    phone=office['phone'],
                                    post_code=office['post_code'],
                                    update_time=updated_date)
            office.save()


def __get_cities_dictionary():
    cities = ShippingCity.objects.all()
    cities_dict = dict((k.external_id, k) for k in cities)
    return cities_dict


@staff_member_required
def shipping_method_detail(request, pk):
    method = get_object_or_404(ShippingMethod, pk=pk)
    return shipping_method_edit(request, method)


@staff_member_required
def shipping_method_delete(request, pk):
    shipping_method = get_object_or_404(ShippingMethod, pk=pk)
    if request.method == 'POST':
        shipping_method.delete()
        messages.success(
            request, _('%(shipping_method_name)s successfully deleted') % {
                'shipping_method_name': shipping_method})
        return redirect('dashboard:shipping-methods')
    ctx = {'shipping_method': shipping_method}
    return TemplateResponse(request, 'dashboard/shipping/method_delete.html', ctx)
