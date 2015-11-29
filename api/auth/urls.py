"""Urls for authentication views"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^google/$', views.google, name='google')
]
