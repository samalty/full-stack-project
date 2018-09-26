from django.conf.urls import url
from .views import index, logout, login, profile, edit_profile

urlpatterns = [
    url(r'^logout/$', logout, name="logout"),
    url(r'^login/$', login, name="login"),
    url(r'^profile/$', profile, name="profile"),
    url(r'^edit_profile/$', edit_profile, name="edit_profile"),
]