from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm

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
        if user:
            auth.login(user=user,request=request)
            return redirect(reverse('profile'))
        else:
            messages.error(request, "Unable to reigster your account at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'index.html', {"registration_form": registration_form})

@login_required
def logout(request):
    """ Logs the user out """
    auth.logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect(reverse('index'))

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
    return render(request, 'login.html', {"login_form": login_form})