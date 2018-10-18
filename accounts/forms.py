from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import UserProfile

class UserLoginForm(forms.Form):
    """ Form used to log users in """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    """ Form used to register new users """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        """ Form validation for email field """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address must be unique')
        return email
    
    def clean_password2(self):
        """ Form validation for password fields """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2:
            raise ValidationError("Please confirm your password")
        if password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

class EditProfileForm(forms.ModelForm):
    """ Form used to edit user profile information """
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'website']

class EditImageForm(forms.ModelForm):
    """ Form used to update profile image """
    class Meta:
        model = UserProfile
        fields = ['image']