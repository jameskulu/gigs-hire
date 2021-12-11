from rest_framework.response import Response
from rest_framework import status
from ...models import Musician


def verify_musician(view_func):
    def wrapper_func(request, *args, **kwargs):
        data = {}
        try:
            musician = Musician.objects.get(email=request.data.get("email"))
        except Musician.DoesNotExist:
            data = {
                "success": False,
                "details": "Invalid Credentials",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if musician.isVerified == True:
            return view_func(request, *args, **kwargs)

        data = {
            "success": False,
            "details": "Your account has not been verified. Please check your email to verify your account.",
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return wrapper_func
