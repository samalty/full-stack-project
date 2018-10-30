from django.conf.urls import url
from django.contrib import admin
from .views import confirm, confirm_payment, checkout, receipt

urlpatterns = [
    url(r'^$', confirm, name='confirm'),
    url(r'^confirm/(?P<id>\d+)', confirm_payment, name='confirm_payment'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^receipt/$', receipt, name='receipt'),
    ]