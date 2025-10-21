from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import random


User = get_user_model()


class SimpleRegisterForm(forms.Form):
    username = forms.CharField(label='Никнейм', max_length=150)
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username'].strip()
        first = self.cleaned_data['first_name'].strip()
        last = self.cleaned_data['last_name'].strip()
        # Если username занят — добавить случайный суффикс
        base = username
        while User.objects.filter(username=username).exists():
            username = f"{base}_{random.randint(100,999)}"
        user = User.objects.create_user(username=username, password=self.cleaned_data['password1'])

    def save(self):
        first = self.cleaned_data['first_name'].strip()
        last = self.cleaned_data['last_name'].strip()
        base = f"{first.lower()}_{last.lower()}"
        username = base
        # обеспечить уникальность username
        i = 0
        while User.objects.filter(username=username).exists():
            i += 1
            username = f"{base}_{random.randint(100,999)}"
        user = User.objects.create_user(username=username, password=self.cleaned_data['password1'])
        user.first_name = first
        user.last_name = last
        user.save()
        return user


class SimpleLoginForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
