from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """ Model for user profile """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400, default='', blank=True)
    location = models.CharField(max_length=100, default='', blank=True)
    website = models.URLField(default='', blank=True)
    image = models.ImageField(upload_to='profile_img', default='anon.png', blank=False)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Profile'
        
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Automatically creates profiles for new users """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()