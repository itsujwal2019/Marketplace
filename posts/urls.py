from django.urls import path
from .views import post_list, post_detail

urlpatterns = [
    path('api/posts/', post_list),
    path('api/posts/<int:pk>/', post_detail),
]
