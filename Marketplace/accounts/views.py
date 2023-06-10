from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from Marketplace.accounts.serializers import RegistrationRequest, RegistrationResponse, LoginRequest, LoginResponse


@swagger_auto_schema(method='POST',
                     request_body=RegistrationRequest,
                     responses={
                         200: openapi.Response('Registration successful', RegistrationResponse),
                         400: 'Bad Request'
                     },
                     tags=['User'])
@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationRequest(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({'message': 'Registration successful',
                         'user': user.username,
                         'access_token': access_token,
                         'refresh_token': refresh_token})
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method='POST',
                     request_body=LoginRequest,
                     responses={
                         200: openapi.Response('Login successful', LoginResponse),
                         400: 'Bad Request'
                     },
                     tags=['User']
                     )
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token})

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user_profile(request):
    user = request.user
    profile_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active':user.is_active
    }
    return Response(profile_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_user_profile(request):
    user_id = request.user.id
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)