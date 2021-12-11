from .serializers import MusicianSerializer, SendMailMusicianSerializer
from Accounts.models import Musician
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings


@api_view(
    [
        "GET",
    ]
)
def musician_view(request):
    musicians = Musician.objects.all().order_by("-createdAt")
    serializer = MusicianSerializer(musicians, many=True, context={"request": request})
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


@api_view(
    [
        "GET",
    ]
)
def single_musician_view(request, pk):
    data = {}
    try:
        musician = Musician.objects.get(pk=pk)
    except Musician.DoesNotExist:
        data = {"success": False, "details": "Musician not found"}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    serializer = MusicianSerializer(musician, context={"request": request})
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
def send_enquiry_musician(request):
    if request.method == "POST":
        data = {}
        serializer = SendMailMusicianSerializer(data=request.data)
        if serializer.is_valid():
            subject = "Enquiry from GigsHire"
            html_message = serializer.validated_data["message"]
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = serializer.validated_data["email"]

            send_mail(
                subject, plain_message, from_email, [to], html_message=html_message
            )

            data = {"success": True, "details": "Enquiry sent successfully"}
            return Response(data, status=status.HTTP_200_OK)

        data = {"success": False, "details": serializer.errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
