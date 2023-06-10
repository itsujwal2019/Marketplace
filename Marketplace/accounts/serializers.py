from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationRequest(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        if len(attrs['password']) < 10:
            raise serializers.ValidationError(
                "Password need to be 10 characters long.")
        return attrs


class RegistrationResponse(serializers.Serializer):
    message = serializers.CharField()
    user = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class LoginRequest(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class LoginResponse(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
