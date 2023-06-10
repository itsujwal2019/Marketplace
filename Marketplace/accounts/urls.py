from django.urls import path
from rest_framework import routers
from Marketplace.accounts.views import registration_view, login_view, get_user_profile, delete_user_profile, change_password

urlpatterns = [
    path('api/register/', registration_view, name='register'),
    path('api/login/', login_view, name='login'),
    path('api/get_user_profile/', get_user_profile, name='get_user_profile'),
    path('api/delete_user_profile/', delete_user_profile, name='delete_user_profile'),
    path('api/change_password/', change_password, name='change_user_password'),
]
