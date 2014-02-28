from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (ProductImage, BagVariant, Bag, ShirtVariant, Shirt,
                     Category, FixedProductDiscount, Color)
from .forms import ShirtAdminForm


class ImageAdminInline(admin.StackedInline):
    model = ProductImage


class BagVariantInline(admin.StackedInline):
    model = BagVariant


class BagAdmin(admin.ModelAdmin):
    inlines = [BagVariantInline, ImageAdminInline]


class ShirtVariant(admin.StackedInline):
    model = ShirtVariant


class ShirtAdmin(admin.ModelAdmin):
    form = ShirtAdminForm
    list_display = ['name', 'collection', 'admin_get_price_min',
                    'admin_get_price_max']
    inlines = [ShirtVariant, ImageAdminInline]


class ProductCollectionAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Bag, BagAdmin)
admin.site.register(Shirt, ShirtAdmin)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(FixedProductDiscount)
admin.site.register(Color)