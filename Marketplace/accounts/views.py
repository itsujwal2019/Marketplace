from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from Marketplace.accounts.serializers import RegistrationRequest, RegistrationResponse, LoginRequest, LoginResponse, ChangePasswordRequest, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


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
    serializer = LoginRequest(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        refresh = RefreshToken.for_user(validated_data)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='GET',
                     responses={
                         200:  UserSerializer
                     },
                     tags=['Profile']
                     )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user_profile(request):
    user = request.user
    profile_data = {
        'id': user.id,
        'username': user.username,
        'type': user.user_type
    }
    return Response(profile_data)


@swagger_auto_schema(method='DELETE',
                     tags=['Profile']
                     )
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


@swagger_auto_schema(method='PUT',
                     request_body=ChangePasswordRequest,
                     responses={
                         204: openapi.Response(description="No Content")
                     },
                     tags=['User']
                     )
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def change_password(request):
    serializer = ChangePasswordRequest(request.user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'You have no right to perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

