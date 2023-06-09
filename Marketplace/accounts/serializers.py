from rest_framework import serializers
from django.contrib.auth.models import User
# from Marketplace.accounts.models import UserProfile


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
            raise serializers.ValidationError("Password need to be 10 characters long.")


class RegistrationResponse(serializers.Serializer):
    message = serializers.CharField()
    user = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
