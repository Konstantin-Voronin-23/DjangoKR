from django.urls import path
from users.apps import UsersConfig
from .views import UserLoginView, UserLogoutView, UserRegisterView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path(
        "logout/",
        UserLogoutView.as_view(next_page="/users/login/?logout=true"),
        name="logout",
    ),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]