from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserProfileForm, UserLoginForm
from .models import User


class UserLoginView(LoginView):
    """Класс контроллера авторизации"""

    template_name = "users/login.html"
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy("mailing:home")


class UserLogoutView(LogoutView):
    """Класс контроллера выхода из учетной записи"""

    next_page = "/users/login/"


class UserRegisterView(CreateView):
    """Класс контроллера регистрации"""

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Класс контроллера профиля пользователя"""

    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user
