from modeltranslation.translator import register, TranslationOptions
from saleor.shipping.models import ShippingMethod, ShippingCity, ShippingOffice


@register(ShippingMethod)
class ShippingMethodTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(ShippingCity)
class ShippingCityTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(ShippingOffice)
class ShippingOfficeTranslationOptions(TranslationOptions):
    fields = ('name', 'address')
