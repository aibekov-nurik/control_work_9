# gallery/api/urls.py

from django.urls import path
from .views import add_to_favorites, remove_from_favorites

urlpatterns = [
    path('favorites/add/', add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/', remove_from_favorites, name='remove_from_favorites'),
]
