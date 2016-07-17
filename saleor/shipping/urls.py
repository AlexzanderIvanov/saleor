from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cities/(?P<city>[0-9]+)/offices/$', views.get_offices),
]
