from django.contrib import admin
from .models import UserProfile

#class UserProfileAdmin(admin.ModelAdmin):
#    list_display = ['user', 'bio', 'location', 'website']

#admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(UserProfile)