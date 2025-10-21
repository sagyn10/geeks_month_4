from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout as django_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from .forms import ApplicantSignUpForm, LoginForm


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = ApplicantSignUpForm

    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        # не логиним пользователя автоматически — отправляем на страницу входа
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm


class CustomLogoutView(LogoutView):
    next_page = '/'

    def get(self, request, *args, **kwargs):
        # разрешаем выход по GET (ссылка "Выйти" в шапке)
        django_logout(request)
        # редирект на next_page или главную
        return redirect(self.next_page or '/')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = getattr(self.request.user, 'profile', None)
        initials = profile.initials() if profile else (self.request.user.username[:2].upper())
        ctx.update({'profile': profile, 'initials': initials})
        return ctx
