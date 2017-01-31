from django.conf.urls import url
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^contacts/', views.contacts, name='contacts'),
    url(r'^about/', views.about, name='about'),
    url(r'^facebook/$', RedirectView.as_view(url='https://facebook.com/ap1ltd/'),
        name='facebook'),
]
