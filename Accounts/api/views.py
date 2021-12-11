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
from ..models import Musician
from .middlewares.musicianVerify import verify_musician
from Category.models import Category


@api_view(
    [
        "POST",
    ]
)
def registration(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            token = secrets.token_hex(16)
            hashed_pwd = make_password(serializer.validated_data["password"])
            account = serializer.save(
                password=hashed_pwd,
                emailToken=token,
                category=Category.objects.get(pk=serializer.validated_data["category"]),
            )

            subject = "Account activation email"
            html_message = f"Please click on this button to activate your account.<a href='{settings.CLIENT_BASE_URL}/verify-email/{token}'><button>I Confirm</button></a>"
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = account.email

            send_mail(
                subject, plain_message, from_email, [to], html_message=html_message
            )

            data["success"] = True
            data["musician"] = {"id": account.id, "email": account.email}
            return Response(data, status=status.HTTP_201_CREATED)

        data = {"success": False, "details": serializer.errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
def activate_account(request):
    if request.method == "POST":
        serializer = ActivateAccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                musician = Musician.objects.get(
                    emailToken=serializer.validated_data["token"]
                )
            except Musician.DoesNotExist:
                data = {
                    "success": False,
                    "details": "Invalid Token",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            musician.emailToken = None
            musician.isVerified = True
            musician.save()

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
@verify_musician
def login(request):
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                musician = Musician.objects.get(
                    email=serializer.validated_data["email"]
                )
            except Musician.DoesNotExist:
                data = {
                    "success": False,
                    "details": "Invalid Credentials",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            if not check_password(
                serializer.validated_data["password"], musician.password
            ):
                data = {
                    "success": False,
                    "details": "Invalid Credentials",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            token = jwt.encode(
                {"id": musician.id}, settings.JWT_SECRET_KEY, algorithm="HS256"
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
                musician = Musician.objects.get(
                    email=serializer.validated_data["email"]
                )
            except Musician.DoesNotExist:
                data = {
                    "success": False,
                    "details": "Email does not exists",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            token = secrets.token_hex(16)

            musician.resetToken = token
            musician.save()

            subject = "Reset password email"
            html_message = f"Please click on this button to change your account password.<a href='{settings.CLIENT_BASE_URL}/reset-password/{token}'><button>Change Password</button></a>"
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = musician.email

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
                musician = Musician.objects.get(
                    resetToken=serializer.validated_data["token"]
                )
            except Musician.DoesNotExist:
                data = {
                    "success": False,
                    "details": "Invalid Token",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            hashed_pwd = make_password(serializer.validated_data["newPassword"])
            musician.resetToken = None
            musician.password = hashed_pwd
            musician.save()

            data = {
                "success": True,
                "details": "New password changed successfully",
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {"success": False, "details": serializer.errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
