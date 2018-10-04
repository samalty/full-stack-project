from django.conf.urls import url
from django.contrib import admin
from .views import user_dashboard, project_detail, plan_project, delete_project, approve_project, sign_off, update_status, edit, launched, status, priority

urlpatterns = [
    url(r'^$', user_dashboard, name='user_dashboard'),
    url(r'^launched/$', launched, name='launched'),
    url(r'^status/$', status, name='status'),
    url(r'^priority/$', priority, name='priority'),
    url(r'^(?P<pk>\d+)/$', project_detail, name='project_detail'),
    url(r'^(?P<pk>\d+)/edit/$', edit, name='edit'),
    url(r'^plan_project/$', plan_project, name='plan_project'),
    url(r'^(?P<pk>\d+)/update_status/$', update_status, name='update_status'),
    url(r'^(?P<pk>\d+)/delete/$', delete_project, name='delete_project'),
    url(r'^(?P<pk>\d+)/approve/$', approve_project, name='approve_project'),
    url(r'^(?P<pk>\d+)/sign_off/$', sign_off, name='sign_off'),
    ]