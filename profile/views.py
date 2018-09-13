from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def profile(request):
    """ Returns the main navigation page """
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {"user": user})