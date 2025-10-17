from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import ApplicantProfile
try:
    from captcha.fields import CaptchaField  # type: ignore
except Exception:
    # если django-simple-captcha не установлен, подставим простой CharField (необязательный)
    from django import forms as _forms

    class CaptchaField(_forms.CharField):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('required', False)
            kwargs.setdefault('label', 'Captcha (disabled)')
            super().__init__(*args, **kwargs)


class ApplicantSignUpForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    first_name = forms.CharField(label='Имя', max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    email = forms.EmailField(label='Почта', required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'}))

    phone = forms.CharField(label='Телефон', required=False,
                            widget=forms.TextInput(attrs={'placeholder': '+996 555 123 456'}))
    address = forms.CharField(label='Адрес', required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Улица, дом, квартира'}))
    city = forms.CharField(label='Город', required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Город'}))
    country = forms.CharField(label='Страна', required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Страна'}))
    linkedin = forms.URLField(label='LinkedIn', required=False,
                              widget=forms.URLInput(attrs={'placeholder': 'https://www.linkedin.com/in/...'}))
    github = forms.URLField(label='GitHub', required=False,
                            widget=forms.URLInput(attrs={'placeholder': 'https://github.com/...'}))
    experience_years = forms.IntegerField(label='Опыт (лет)', required=False, min_value=0,
                                          widget=forms.NumberInput(attrs={'placeholder': 'Например, 2'}))
    desired_position = forms.CharField(label='Желаемая должность', required=False,
                                       widget=forms.TextInput(attrs={'placeholder': 'Frontend, Backend...'}))
    resume = forms.CharField(label='Резюме', widget=forms.Textarea(attrs={'placeholder': 'Краткое описание опыта'}), required=False)
    portfolio_url = forms.URLField(label='Портфолио (URL)', required=False,
                                   widget=forms.URLInput(attrs={'placeholder': 'https://portfolio.example.com'}))

    captcha = CaptchaField(label='Капча', required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'phone', 'address', 'city', 'country', 'linkedin', 'github',
                  'experience_years', 'desired_position', 'resume', 'portfolio_url', 'captcha')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            ApplicantProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data.get('phone', ''),
                    'address': self.cleaned_data.get('address', ''),
                    'city': self.cleaned_data.get('city', ''),
                    'country': self.cleaned_data.get('country', ''),
                    'linkedin': self.cleaned_data.get('linkedin', ''),
                    'github': self.cleaned_data.get('github', ''),
                    'experience_years': self.cleaned_data.get('experience_years') or 0,
                    'desired_position': self.cleaned_data.get('desired_position', ''),
                    'resume': self.cleaned_data.get('resume', ''),
                    'portfolio_url': self.cleaned_data.get('portfolio_url', ''),
                }
            )
        return user


class LoginForm(AuthenticationForm):
    # расширяем стандартную форму логина капчей и русскими метками
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя или email'})
        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})
        # добавляем капчу если поле определено выше (CaptchaField может быть в модуле)
        try:
            self.fields['captcha'] = CaptchaField(label='Капча', required=False)
        except Exception:
            # если captcha не доступна — ничего не делаем
            pass
