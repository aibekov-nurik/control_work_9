# gallery/urls.py

from django.urls import path
from .views import (
    photo_list, photo_detail, PhotoCreateView, PhotoUpdateView, PhotoDeleteView,
    AlbumCreateView, AlbumUpdateView, AlbumDeleteView, album_detail, generate_access_token, photo_by_token,

)

urlpatterns = [
    path('', photo_list, name='photo_list'),
    path('photo/<int:id>/', photo_detail, name='photo_detail'),
    path('photo/create/', PhotoCreateView.as_view(), name='create_photo'),
    path('photo/<int:pk>/edit/', PhotoUpdateView.as_view(), name='edit_photo'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete_photo'),

    path('album/<int:id>/', album_detail, name='album_detail'),
    path('album/create/', AlbumCreateView.as_view(), name='create_album'),
    path('album/<int:pk>/edit/', AlbumUpdateView.as_view(), name='edit_album'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='delete_album'),
    path('photo/<int:id>/generate_token/', generate_access_token, name='generate_access_token'),
    path('photo/<str:token>/', photo_by_token, name='photo_by_token'),
]
