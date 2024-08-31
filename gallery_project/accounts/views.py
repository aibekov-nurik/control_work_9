# accounts/views.py

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from gallery.models import Photo, Album

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('photo_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('photo_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('photo_list')

@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    public_albums = Album.objects.filter(author=user, is_public=True)
    public_photos = Photo.objects.filter(author=user, album__isnull=True, is_public=True)

    if request.user == user:
        private_albums = Album.objects.filter(author=user, is_public=False)
        private_photos = Photo.objects.filter(author=user, album__isnull=True, is_public=False)
    else:
        private_albums = private_photos = None

    return render(request, 'profile.html', {
        'profile_user': user,
        'public_albums': public_albums,
        'public_photos': public_photos,
        'private_albums': private_albums,
        'private_photos': private_photos,
    })

@login_required
def favorites(request):
    user = request.user
    favorite_photos = user.favorite_photos.filter(is_public=True)
    favorite_albums = user.favorite_albums.filter(is_public=True)

    return render(request, 'favorites.html', {
        'favorite_photos': favorite_photos,
        'favorite_albums': favorite_albums,
    })
