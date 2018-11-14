from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm, EditProfileForm, EditImageForm
from accounts.models import UserProfile
from blog.models import Post

def index(request):
    """ Returns the index and registration page """
    if request.user.is_authenticated:
        return redirect(profile, user.pk)
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            # UserProfile.objects.create(user=user)
        if user:
            auth.login(user=user,request=request)
            return redirect(profile, user.pk)
        else:
            messages.error(request, "Sorry. We are unable to register your account at this time.")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'index.html', {'registration_form': registration_form})

@login_required
def logout(request):
    """ Logs the user out """
    auth.logout(request)
    messages.success(request, "Thanks for dropping by. See you again soon.")
    return redirect(reverse('login'))

def login(request):
    """ Returns the login page """
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                return redirect(profile, user.pk)
            else:
                login_form.add_error(None, "Sorry. The username and password \
                combination that you entered wasn't recognised.")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})

@login_required
def profile(request, pk):
    """ Returns the main navigation page """
    user = User.objects.get(email=request.user.email, pk=pk)
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request, pk):
    """ Presents a form enabling user to edit their profile """
    user = User.objects.get(email=request.user.email, pk=pk)
    post = get_object_or_404(UserProfile, pk=pk) if pk else None
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            post = form.save()
            return redirect(profile, user.pk)
    else:
        form = EditProfileForm(instance=post)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def update_image(request, pk):
    """ Presents a form enabling user to update their profile image """
    user = User.objects.get(email=request.user.email, pk=pk)
    post = get_object_or_404(UserProfile, pk=pk) if pk else None
    if request.method == "POST":
        form = EditImageForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            post = form.save()
            return redirect(profile, user.pk)
    else:
        form = EditImageForm(instance=post)
    return render(request, 'update_image.html', {'form': form})

@login_required
def display_profile(request, slug):
    """ Renders a page where users can view other users' profiles """
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'display_profile.html', {'post': post})