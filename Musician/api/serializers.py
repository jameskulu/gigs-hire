from rest_framework import serializers
from Accounts.models import Musician
from Category.api.serializers import CategorySerializer


class MusicianSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Musician
        exclude = (
            "password",
            "emailToken",
            "emailTokenExpireDate",
            "resetToken",
            "resetTokenExpireDate",
        )


class SendMailMusicianSerializer(serializers.Serializer):
    recipient = serializers.EmailField(required=True)
    email = serializers.EmailField(required=True)
    message = serializers.CharField(required=True)
