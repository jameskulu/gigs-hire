import jwt
import secrets
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    ActivateAccountSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from ..models import User
from .middlewares.userVerify import verify_user


@api_view(
    [
        "POST",
    ]
)
def user_registration(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            token = secrets.token_hex(16)
            hashed_pwd = make_password(serializer.validated_data["password"])
            account = serializer.save(password=hashed_pwd, emailToken=token)

            subject = "Account activation email"
            html_message = f"Please click on this button to activate your account.<a href='http://localhost:3000/verify-email/{token}'><button>I Confirm</button></a>"
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = account.email

            send_mail(
                subject, plain_message, from_email, [to], html_message=html_message
            )

            data["success"] = True
            data["user"] = {"id": account.id, "email": account.email}
            return Response(data, status=status.HTTP_201_CREATED)

        data = {"success": False, "details": serializer.errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
def user_activate_account(request):
    if request.method == "POST":
        serializer = ActivateAccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                user = User.objects.get(emailToken=serializer.validated_data["token"])
            except User.DoesNotExist:
                data = {
                    "success": False,
                    "details": "Invalid Token",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            user.emailToken = None
            user.isVerified = True
            user.save()

            data = {
                "success": True,
                "details": "Account has been verified.",
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {"success": False, "details": serializer.errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
@verify_user
def user_login(request):
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data["email"])
            except User.DoesNotExist:
                data = {
                    "success": False,
                    "details": "Invalid Credentials",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            if not check_password(serializer.validated_data["password"], user.password):
                data = {
                    "success": False,
                    "details": "Invalid Credentials",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            token = jwt.encode(
                {"id": user.id}, settings.JWT_SECRET_KEY, algorithm="HS256"
            )

            data = {
                "success": True,
                "token": token,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        data = {"success": False, "details": serializer.errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
def forgot_password(request):
    if request.method == "POST":
        serializer = ForgotPasswordSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data["email"])
            except User.DoesNotExist:
                data = {
                    "success": False,
                    "details": "Email does not exists",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            token = secrets.token_hex(16)

            user.resetToken = token
            user.save()

            subject = "Reset password email"
            html_message = f"Please click on this button to change your account password.<a href='http://localhost:3000/reset-password/{token}'><button>Change Password</button></a>"
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = user.email

            send_mail(
                subject, plain_message, from_email, [to], html_message=html_message
            )

            data = {
                "success": True,
                "details": "Reset password email sent.",
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {"success": False, "details": serializer.errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
def reset_password(request):
    if request.method == "POST":
        serializer = ResetPasswordSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                user = User.objects.get(resetToken=serializer.validated_data["token"])
            except User.DoesNotExist:
                data = {
                    "success": False,
                    "details": "Invalid Token",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            hashed_pwd = make_password(serializer.validated_data["newPassword"])
            user.resetToken = None
            user.password = hashed_pwd
            user.save()

            data = {
                "success": True,
                "details": "New password changed successfully",
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {"success": False, "details": serializer.errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
