from django.conf.urls import url
from django.contrib import admin
from .views import index, logout, login, profile, edit_profile, display_profile, update_image

urlpatterns = [
    url(r'^logout/$', logout, name="logout"),
    url(r'^login/$', login, name="login"),
    url(r'^(?P<pk>\d+)/$', profile, name="profile"),
    url(r'^(?P<pk>\d+)/edit/$', edit_profile, name="edit_profile"),
    url(r'^(?P<pk>\d+)/update_image/$', update_image, name="update_image"),
    url(r'^(?P<slug>[\w-]+)/author/$', display_profile, name="display_profile"),
]