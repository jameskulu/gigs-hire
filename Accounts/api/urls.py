from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.user_registration, name="user-registration"),
    path(
        "email-activate/",
        views.user_activate_account,
        name="user-activate-account",
    ),
    path("login/", views.user_login, name="user-login"),
    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("reset-password/", views.reset_password, name="reset-password"),
]
