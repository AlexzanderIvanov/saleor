from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from .cart.urls import urlpatterns as cart_urls
from .checkout.urls import urlpatterns as checkout_urls
from .core.sitemaps import sitemaps
from .core.urls import urlpatterns as core_urls
from .dashboard.urls import urlpatterns as dashboard_urls
from .order.urls import urlpatterns as order_urls
from .product.urls import urlpatterns as product_urls
from .registration.urls import urlpatterns as registration_urls
from .userprofile.urls import urlpatterns as userprofile_urls
from .shipping.urls import urlpatterns as shipping_urls

admin.autodiscover()

urlpatterns = [
    url(r'^', include(core_urls)),
    url(r'^account/', include(registration_urls, namespace='registration')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cart/', include(cart_urls, namespace='cart')),
    url(r'^checkout/', include(checkout_urls, namespace='checkout')),
    url(r'^dashboard/', include(dashboard_urls, namespace='dashboard')),
    url(r'^order/', include(order_urls, namespace='order')),
    url(r'^products/', include(product_urls, namespace='product')),
    url(r'^profile/', include(userprofile_urls, namespace='profile')),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'', include('payments.urls')),
    url(r'^shipping/', include(shipping_urls, namespace='shipping')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT})]
if not settings.DEBUG:
    urlpatterns += url('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
