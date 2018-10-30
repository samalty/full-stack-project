from django.conf.urls import url
from django.contrib import admin
from .views import confirm, confirm_payment, checkout, receipt

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', confirm, name='confirm'),
    # url(r'^$', confirm, name='confirm'),
    #url(r'^confirm/(?P<pk>\d)', confirm_payment, name='confirm_payment'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^receipt/(?P<pk>\d)', receipt, name='receipt'),
    ]



















