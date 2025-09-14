from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import User


class UserRegisterForm(UserCreationForm):
    """Класс создания формы регистрации пользователя"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserProfileForm(UserChangeForm):
    """Класс создания формы профиля пользователя"""

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "avatar", "country")
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Введите ваш email"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите ваше имя"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите вашу фамилию"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+7 (999) 999-99-99"
            }),
            "country": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите вашу страну"
            }),
            "avatar": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
        self.fields["avatar"].required = False


class UserLoginForm(AuthenticationForm):
    """Класс создания формы авторизации пользователя"""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите ваш email"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )
