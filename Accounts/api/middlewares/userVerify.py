from rest_framework.response import Response
from rest_framework import status
from ...models import User


def verify_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        data = {}
        try:
            user = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            data = {
                "success": False,
                "details": "Invalid Credentials",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if user.isVerified == True:
            return view_func(request, *args, **kwargs)
        
        data = {
                "success": False,
                "details": "Your account has not been verified. Please check your email to verify your account.",
            }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return wrapper_func
