from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from .forms import ApplicantSignUpForm, LoginForm


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = ApplicantSignUpForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:profile')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm


class CustomLogoutView(LogoutView):
    next_page = '/'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = getattr(self.request.user, 'profile', None)
        initials = profile.initials() if profile else (self.request.user.username[:2].upper())
        ctx.update({'profile': profile, 'initials': initials})
        return ctx
