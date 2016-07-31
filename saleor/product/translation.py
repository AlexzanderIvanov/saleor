from modeltranslation.translator import register, TranslationOptions
from saleor.product.models import Category, Product, ProductVariant


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
        fields = ('name', 'description',)


@register(ProductVariant)
class ProductVariantTranslationOptions(TranslationOptions):
        fields = ('name', 'sku')
