from django.urls import path
from . import views

urlpatterns = [
    path('users/<int:user_id>/block/', views.block_unblock_user, name='block_unblock_user'),
    path('users/<int:user_id>/follow/', views.follow_unfollow_user, name='follow_unfollow_user'),

]
