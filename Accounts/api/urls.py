from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registration, name="registration"),
    path(
        "email-activate/",
        views.activate_account,
        name="activate-account",
    ),
    path("login/", views.login, name="login"),
    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("reset-password/", views.reset_password, name="reset-password"),
]
