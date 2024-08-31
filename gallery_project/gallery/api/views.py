# gallery/api/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Photo, Album, Favorite

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    user = request.user
    photo_id = request.data.get('photo_id')
    album_id = request.data.get('album_id')

    if photo_id:
        photo = Photo.objects.get(id=photo_id)
        favorite, created = Favorite.objects.get_or_create(user=user, photo=photo)
        if not created:
            return Response({'error': 'Photo is already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
    elif album_id:
        album = Album.objects.get(id=album_id)
        favorite, created = Favorite.objects.get_or_create(user=user, album=album)
        if not created:
            return Response({'error': 'Album is already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success': 'Added to favorites'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_favorites(request):
    user = request.user
    photo_id = request.data.get('photo_id')
    album_id = request.data.get('album_id')

    if photo_id:
        try:
            favorite = Favorite.objects.get(user=user, photo_id=photo_id)
            favorite.delete()
        except Favorite.DoesNotExist:
            return Response({'error': 'Photo not in favorites'}, status=status.HTTP_400_BAD_REQUEST)
    elif album_id:
        try:
            favorite = Favorite.objects.get(user=user, album_id=album_id)
            favorite.delete()
        except Favorite.DoesNotExist:
            return Response({'error': 'Album not in favorites'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success': 'Removed from favorites'}, status=status.HTTP_200_OK)
