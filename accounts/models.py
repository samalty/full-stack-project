from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """ Model for user profile """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400, default='', blank=True)
    location = models.CharField(max_length=100, default='', blank=True)
    website = models.URLField(default='', blank=True)
    image = models.ImageField(upload_to='profile_img', default='profile_img/anon.png', blank=False)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Profile'