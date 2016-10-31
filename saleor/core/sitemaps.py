from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from ..product.models import Product, Category


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Product.objects.only('id', 'name').order_by('-id')


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        return Category.objects.only('id', 'name').order_by('-id')


class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return ['home', 'contacts']

    def location(self, item):
        return reverse(item)


sitemaps = {'static': StaticViewSitemap, 'products': ProductSitemap, 'categories': CategorySitemap}
