from django.template.response import TemplateResponse

from ..product.models import Product


def home(request):
    products = Product.objects.get_available_products()[:12]
    products = products.prefetch_related('categories', 'images',
                                         'variants__stock')
    return TemplateResponse(
        request, 'base.html',
        {'products': products, 'parent': None})


def contacts(request):
    return TemplateResponse(
        request, 'about/contacts.html')


def delivery(request):
    return TemplateResponse(
        request, 'about/delivery.html')


def about(request):
    return TemplateResponse(
        request, 'about/about.html')
