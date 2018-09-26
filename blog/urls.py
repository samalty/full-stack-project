from django.conf.urls import url
from django.contrib import admin
from .views import get_posts, post_detail, create_or_edit_post, delete_post, PostLikeToggle

urlpatterns = [
    url(r'^$', get_posts, name='get_posts'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='post_detail'),
    url(r'^(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like_toggle'),
    url(r'^/new/$', create_or_edit_post, name='new_post'),
    url(r'^(?P<slug>[\w-]+)/edit/$', create_or_edit_post, name='edit_post'),
    url(r'^(?P<slug>[\w-]+)/delete/$', delete_post, name='delete_post'),
    ]