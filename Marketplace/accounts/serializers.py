from rest_framework import serializers
from django.contrib.auth.models import User


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


class RegistrationResponse(serializers.Serializer):
    message = serializers.CharField()
    user = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
