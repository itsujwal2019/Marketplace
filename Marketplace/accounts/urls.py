from django.urls import path
from rest_framework import routers
from Marketplace.accounts.views import registration_view, login_view

urlpatterns = [
    path('api/register/', registration_view, name='register'),
    path('api/login/', login_view, name='login'),
]
