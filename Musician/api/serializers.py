from rest_framework import serializers
from Accounts.models import Musician


class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musician
        fields = ["firstName", "lastName", "email"]


class SendMailMusicianSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    message = serializers.CharField(required=True)
