from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm, EditProfileForm
from accounts.models import UserProfile

def index(request):
    """ Returns the index and registration page """
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            UserProfile.objects.create(user=user)
        if user:
            auth.login(user=user,request=request)
            return redirect(reverse('profile'))
        else:
            messages.error(request, "Sorry. We are unable to reigster your account at this time.")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'index.html', {'registration_form': registration_form})



@login_required
def logout(request):
    """ Logs the user out """
    auth.logout(request)
    messages.success(request, "Thanks for dropping by. See you again soon :)")
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
                return redirect(reverse('profile'))
            else:
                login_form.add_error(None, "Sorry. The username and password \
                combination that you entered wasn't recognised.")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})

@login_required
def profile(request):
    """ Returns the main navigation page """
    user = User.objects.get(email=request.user.email)
    username = User.objects.get(username=request.user.username)
    return render(request, 'profile.html', {'user': user, 'username': username})

@login_required
def edit_profile(request, pk=None):
    """ Presents a form enabling user to edit their profile """
    post = get_object_or_404(UserProfile, pk=pk) if pk else None
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            post = form.save()
            return redirect(reverse('profile'))
    else:
        form = EditProfileForm(instance=post)
    return render(request, 'edit_profile.html', {'form': form})