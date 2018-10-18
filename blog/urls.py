from django.conf.urls import url
from django.contrib import admin
from .views import get_posts, post_detail, create_or_edit_post, delete_post, PostLike

urlpatterns = [
    url(r'^$', get_posts, name='get_posts'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='post_detail'),
    url(r'^(?P<slug>[\w-]+)/like/$', PostLike.as_view(), name='like'),
    url(r'^/new/$', create_or_edit_post, name='new_post'),
    url(r'^(?P<slug>[\w-]+)/edit/$', create_or_edit_post, name='edit_post'),
    url(r'^(?P<slug>[\w-]+)/delete/$', delete_post, name='delete_post'),
    ]