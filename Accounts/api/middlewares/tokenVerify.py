import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from ...models import Musician


def verify_token(view_func):
    def wrapper_func(request, *args, **kwargs):
        data = {}
        auth_data = request.META.get("HTTP_AUTHORIZATION")

        if not auth_data:
            data = {
                "success": False,
                "details": "Missing Authorization Header",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        prefix, token = auth_data.split(" ")

        if not token:
            data = {
                "success": False,
                "details": "No authentication token, authorization denied",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            verified = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            request.user = verified
            return view_func(request, *args, **kwargs)
        except jwt.exceptions.DecodeError:
            data = {
                "success": False,
                "details": "Invalid Token",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return wrapper_func


# class JWTAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         auth_data = authentication.get_authorization_header(request)

#         if not auth_data:
#             return None

#         prefix, token = auth_data.decode("utf-8").split(" ")

#         # try:
#         payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
#         musician = Musician.objects.get(id=payload["id"])
#         return (musician, token)

#         # except jwt.DecodeError as identifier:
#         #     raise exceptions.AuthenticationFailed("Your token is invalid")
#         # except jwt.ExpiredSignatureError as identifier:
#         #     raise exceptions.AuthenticationFailed("Your token is expired")

#         # return super().authenticate(request)
