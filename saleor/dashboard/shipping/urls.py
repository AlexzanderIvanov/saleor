from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.shipping_method_list, name='shipping-methods'),
    url(r'^add/$', views.shipping_method_add, name='shipping-method-add'),
    url(r'^(?P<pk>\d+)/$', views.shipping_method_detail, name='shipping-method-detail'),
    url(r'^(?P<pk>\d+)/delete/$',
        views.shipping_method_delete, name='shipping-method-delete'),
    url(r'^countries/$', views.shipping_countries_list, name='countries-list'),
    url(r'^countries/add/$', views.shipping_country_add, name='shipping-country-add'),
    url(r'^cities/$', views.shipping_cities_list, name='shipping-cities-list'),
    url(r'^cities/load/$', views.shipping_cities_load, name='shipping-cities-load'),
    url(r'^offices/$', views.shipping_offices_list, name='shipping-offices-list'),
    url(r'^offices/load/$', views.shipping_offices_load, name='shipping-offices-load'),
]
