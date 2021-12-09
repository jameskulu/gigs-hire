from rest_framework import serializers
from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["firstName", "lastName", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    # def validate(self, data):
    #     password = data.get('password')
    #     password2 = data.get('password2')
    #     if password != password2:
    #         raise serializers.ValidationError({'password': 'Two Password fields must match.'})
    #     return data

    # def save(self):
    #     user = User(
    #         email=self.validated_data['email'],
    #     )
    #     password = self.validated_data['password']
    #     password2 = self.validated_data['password2']

    #     if password != password2:
    #         raise serializers.ValidationError(
    #             {'password': 'Two Password fields must match.'})
    #     user.password = password
    #     user.save()
    #     return user


class ActivateAccountSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=5, write_only=True)
    email = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ["email", "password"]
