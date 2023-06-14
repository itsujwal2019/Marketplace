from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


@swagger_auto_schema(method='GET',
                     tags=['Profile']
                     )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def block_unblock_user(request, user_id):
    try:
        user_to_modify = User.objects.get(pk=user_id)
        user = request.user

        if user == user_to_modify:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user_to_modify in user.blocked_by.all():
            user.blocked_by.remove(user_to_modify)
        else:
            user.blocked_by.add(user_to_modify)

        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='POST',
                     tags=['Profile']
                     )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def follow_unfollow_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_to_modify = request.user  

        if user == user_to_modify:
            # same user 
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user_to_modify in user.following.all():
            user.following.remove(user_to_modify)
        else:
            user.following.add(user_to_modify)

        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
