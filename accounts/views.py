from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import ApplicantSignUpForm, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = ApplicantSignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    profile = getattr(request.user, 'profile', None)
    initials = profile.initials() if profile else (request.user.username[:2].upper())
    return render(request, 'accounts/profile.html', {'profile': profile, 'initials': initials})
