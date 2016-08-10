from modeltranslation.translator import register, TranslationOptions
from saleor.shipping.models import ShippingMethod


@register(ShippingMethod)
class ShippingMethodTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)
