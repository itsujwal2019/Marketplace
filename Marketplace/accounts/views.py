from Marketplace.accounts.serializers import RegistrationRequest, RegistrationResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi

@swagger_auto_schema(method='POST', request_body=RegistrationRequest, responses={
    200: openapi.Response('Registration successful', RegistrationResponse),
    400: 'Bad Request'
})
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
