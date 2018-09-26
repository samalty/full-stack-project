from django.conf.urls import url
from django.contrib import admin
from .views import user_dashboard, client_dashboard, client_project_detail, project_detail, plan_project, delete_project, approve_project, sign_off

urlpatterns = [
    url(r'^$', user_dashboard, name='user_dashboard'),
    url(r'^client_dashboard/$', client_dashboard, name='client_dashboard'),
    url(r'^client/(?P<pk>\d+)/$', client_project_detail, name='client_project_detail'),
    url(r'^(?P<pk>\d+)/$', project_detail, name='project_detail'),
    url(r'^plan_project/$', plan_project, name='plan_project'),
    url(r'^(?P<pk>\d+)/delete/$', delete_project, name='delete_project'),
    url(r'^(?P<pk>\d+)/approve/$', approve_project, name='approve_project'),
    url(r'^(?P<pk>\d+)/sign_off/$', sign_off, name='sign_off'),
    ]