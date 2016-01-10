"""Urls for Show-related views"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<show_id>\d+)/follow$', views.follow, name='follow')
]
