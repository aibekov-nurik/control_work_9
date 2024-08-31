# gallery/views.py
from audioop import reverse
from msilib.schema import ListView

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import Photo, Album

def index(request):
    photos = Photo.objects.filter(is_public=True)
    albums = Album.objects.filter(is_public=True)
    return render(request, 'index.html', {'photos': photos, 'albums': albums})

@login_required
def photo_detail(request, id):
    photo = get_object_or_404(Photo, id=id)
    if not photo.is_public and request.user != photo.author:
        return render(request, 'forbidden.html')  # Шаблон для отказа в доступе

    favorited_by = photo.favorited_by.all()  # Допустим, у вас есть отношение ManyToMany для избранного
    return render(request, 'photo_detail.html', {'photo': photo, 'favorited_by': favorited_by})


def photo_list(request):
    photos = Photo.objects.filter(is_public=True).order_by('-created_at')
    paginator = Paginator(photos, 10)  # 10 фото на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'photo_list.html', {'page_obj': page_obj})

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'album', 'is_public']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(author=self.user)

    def clean(self):
        cleaned_data = super().clean()
        album = cleaned_data.get('album')
        is_public = cleaned_data.get('is_public')
        if album and not album.is_public and is_public:
            self.add_error('is_public', 'Невозможно сделать фотографию публичной, если альбом приватный.')
        return cleaned_data

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo_form.html'
    success_url = reverse_lazy('photo_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photo_form.html'
    success_url = reverse_lazy('photo_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Photo.objects.filter(author=self.request.user)
    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.author or self.request.user.has_perm('gallery.change_photo')

class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = 'photo_confirm_delete.html'
    success_url = reverse_lazy('photo_list')

    def get_queryset(self):
        return Photo.objects.filter(author=self.request.user)

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.author or self.request.user.has_perm('gallery.delete_photo')

def album_detail(request, id):
    album = get_object_or_404(Album, id=id, is_public=True)
    photos = album.photo_set.filter(is_public=True).order_by('-created_at')
    paginator = Paginator(photos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'album_detail.html', {'album': album, 'page_obj': page_obj})

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album_form.html'
    success_url = reverse_lazy('album_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album_form.html'
    success_url = reverse_lazy('album_list')

    def get_queryset(self):
        return Album.objects.filter(author=self.request.user)

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.author or self.request.user.has_perm('gallery.change_album')

class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'album_confirm_delete.html'
    success_url = reverse_lazy('album_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.photo_set.all().delete()  # Удаление всех фото в альбоме
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Album.objects.filter(author=self.request.user)

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.author or self.request.user.has_perm('gallery.delete_album')

@login_required
def generate_access_token(request, id):
    photo = get_object_or_404(Photo, id=id, author=request.user)
    if not photo.access_token:
        photo.generate_access_token()
    return redirect(reverse('photo_detail', kwargs={'id': id}))

def photo_by_token(request, token):
    photo = get_object_or_404(Photo, access_token=token)
    return render(request, 'photo_detail.html', {'photo': photo})

