from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    """ Model for individual blog posts """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    views = models.IntegerField(default=0)
    tag = models.CharField(max_length=30, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title