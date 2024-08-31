# accounts/urls.py

from django.urls import path
from .views import register, user_login, user_logout, profile, favorites

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('favorites/', favorites, name='favorites'),
]
