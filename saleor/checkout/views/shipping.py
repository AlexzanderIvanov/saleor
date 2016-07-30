from decimal import Decimal

from django.conf import settings
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from prices import Price

from ..forms import AnonymousUserShippingForm, ShippingAddressesForm
from ...remoteecont import RemoteEcontXml
from ...remoteecont.transfer import CurlTransfer
from ...userprofile.forms import AddressForm
from ...userprofile.models import Address

econt = RemoteEcontXml(settings.SERVICE_URL, settings.PARCEL_URL,  # Remote API urls
                       'itpartner', 'itpartner',  # Username and password
                       CurlTransfer)


def anonymous_user_shipping_address_view(request, checkout):
    data = request.POST or None
    shipping_address = checkout.shipping_address
    address = Address(country='BG')
    if shipping_address is not None:
        address_form = AddressForm(
            data, instance=checkout.shipping_address, autocomplete_type='shipping')
    else:
        address_form = AddressForm(
            data, autocomplete_type='shipping', initial=request.country, instance=address)
    user_form = AnonymousUserShippingForm(data, initial={'email': checkout.email})
    if user_form.is_valid() and address_form.is_valid():
        checkout.shipping_address = address_form.instance
        shipping_price = calc_shipping_costs(checkout.shipping_address, checkout)
        checkout.shipping_price = shipping_price
        checkout.email = user_form.cleaned_data['email']
        return redirect('checkout:shipping-method')
    return TemplateResponse(
        request, 'checkout/shipping_address.html', context={
            'address_form': address_form, 'user_form': user_form, 'checkout': checkout})


def user_shipping_address_view(request, checkout):
    data = request.POST or None
    additional_addresses = request.user.addresses.all()
    checkout.email = request.user.email
    shipping_address = checkout.shipping_address
    address = Address(country='BG')

    if shipping_address is not None and shipping_address.id:
        address_form = AddressForm(
            data, autocomplete_type='shipping', initial=request.country, instance=address)
        addresses_form = ShippingAddressesForm(
            data, additional_addresses=additional_addresses,
            initial={'address': shipping_address.id})
    elif shipping_address:
        address_form = AddressForm(data, initial=request.country, instance=shipping_address)
        addresses_form = ShippingAddressesForm(
            data, additional_addresses=additional_addresses)
    else:
        address_form = AddressForm(data, initial=request.country, instance=address)
        addresses_form = ShippingAddressesForm(
            data, additional_addresses=additional_addresses)

    if addresses_form.is_valid():
        if addresses_form.cleaned_data['address'] != ShippingAddressesForm.NEW_ADDRESS:
            address_id = addresses_form.cleaned_data['address']
            checkout.shipping_address = Address.objects.get(id=address_id)
        elif address_form.is_valid():
            checkout.shipping_address = address_form.instance
        shipping_price = calc_shipping_costs(checkout.shipping_address, checkout)
        checkout.shipping_price = shipping_price
        checkout.get_total()
        return redirect('checkout:shipping-method')
    return TemplateResponse(
        request, 'checkout/shipping_address.html', context={
            'address_form': address_form, 'user_form': addresses_form,
            'checkout': checkout, 'additional_addresses': additional_addresses})


def calc_shipping_costs(address, checkout):
    receiver = _prepare_receiver(address)
    shipment = _prepare_shipment(address, checkout)
    services = _prepare_additional_services(checkout.cart)
    request = dict(receiver)
    request.update(shipment)
    request.update(services)
    response = econt.shipping(request,
                              {'validate': '0', 'response_type': 'XML', 'only_calculate': '1',
                               'process_all_parcels': '1'})
    result = response.get('result').get('e')
    error = result.get('error')  # handle error
    loading_price = result.get('loading_price')
    price_str = Decimal(loading_price.get('total'))
    return Price(price_str, currency=settings.DEFAULT_CURRENCY)


def _prepare_receiver(address):
    street, street_other, office_code = ('', '', '')
    if address.to_office:
        office_code = address.office.office_code
    else:
        street = address.street_address_1
        street_other = address.street_address_2
    receiver = {'receiver': {
        'city': address.city.name,  # Абсолютно същото като
        'post_code': address.postal_code,  # за подателя
        'office_code': office_code,
        'name': address.first_name,
        'name_person': address.last_name,
        'receiver_email': '',
        'quarter': '',
        'street': street,
        'street_num': '',
        'street_bl': '',
        'street_vh': '',
        'street_et': '',
        'street_ap': '',
        'street_other': street_other,
        'phone_num': address.phone}}
    return receiver


def _prepare_shipment(address, checkout):
    weight = _calculate_weight(checkout.cart)
    tariff_sub_code = 'OFFICE_OFFICE' if address.to_office else 'OFFICE_DOOR'
    shipment = {'shipment': {
        'envelope_num': '',  # номер опаковка?!

        # тип пратка, едно от следните:
        # PACK, DOCUMENT, PALLET, CARGO,
        # DOCUMENTPALLET
        'shipment_type': 'PACK',
        'description': '',  # описание
        'pack_count': '1',  # брой пакети?!
        'weight': weight,  # тегло (В КИЛОГРАМИ)
        'tariff_code': '',  # МИСТИКА!
        'tariff_sub_code': tariff_sub_code,  # DOOR_OFFICE, D_D, O_D, O_O
        'pay_after_accept': '1',  # плащане след получаване?
        'pay_after_test': '1',  # плащане след проба
        'delivery_day': ''  # ЗАГАДКА!
    }}
    return shipment


def _prepare_additional_services(cart):
    price = cart.get_total()
    services = {'services': {
        # наложен платеж

        # Малко е безумен тоя начин за представяне на
        # атрибутите, честно казано... не помня вече какво съм
        # си мислил тогава и що така съм го оставил; пък и не
        # е добра абстракция на ХМЛ, FIXME :) По–добре би било
        # атрибутите да отиват в речници с този синтаксис:
        # таг__имеНаАтрибута = {...}
        'cd': {'__content__': str(price.gross),
               '__attrib__': {'type': 'GET'}},
        'cd_agreement_num': '',  # споразумение за защита НП
        'cd_curreny': 'BGN',  # валута
        'dc': '',  # обратна разписка
        'dc_cp': '',  # стокова разписка
        'oc': '',  # обявена стойност
        'oc_currency': '',  # валута на `oc`
    }}
    return services


def _calculate_weight(cart):
    weight = 0
    for line in cart:
        line_weight = line.quantity * _get_product_weight(line.product)
        weight += line_weight
    return weight


def _get_product_weight(product_variant):
    if product_variant.weight_override:
        return product_variant.weight_override
    else:
        return product_variant.product.weight
