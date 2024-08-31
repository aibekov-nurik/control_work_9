# gallery/models.py
import secrets

from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    access_token = models.CharField(max_length=100, blank=True, null=True, unique=True)


    def __str__(self):
        return self.caption
    def generate_access_token(self):
        if not self.access_token:
            self.access_token = secrets.token_urlsafe(16)
            self.save()

User.add_to_class('favorite_photos', models.ManyToManyField(Photo, related_name='favorited_by'))

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ['user', 'photo', 'album']