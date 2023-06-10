from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

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
        if len(attrs['password']) < 6:
            raise serializers.ValidationError(
                "Password need to be 6 characters long.")
        return attrs


class RegistrationResponse(serializers.Serializer):
    message = serializers.CharField()
    user = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class LoginRequest(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    type = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Username doesnot exists.")
        return user



class LoginResponse(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type' ]


# TODO make it more better idk how. It keep changing password 
# TODO maybe because of bearer token
class ChangePasswordRequest(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def update(self, instance, validated_data):
        current_password = validated_data.get("current_password")
        new_password = validated_data.get("new_password")
        user = User.objects.get(id=instance.id) 
        check_password = user.check_password(current_password)

        if check_password:
            user.set_password(new_password)
            user.save()
            return user
        else:
            return serializers.ValidationError("Your current password is invalid.")
