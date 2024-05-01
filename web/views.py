from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import PlaylistForm, SongForm
from .models import Playlist, Song, Artist
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class CheckIsOwnerMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(CheckIsOwnerMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

class LoginRequiredCheckIsOwnerUpdateView(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
    template_name ='form.html'
class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    template_name = 'form.html'
    form_class = PlaylistForm

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assignem l'usuari actual a la llista de reproducció
        return super(PlaylistCreate, self).form_valid(form)

class PlaylistDetail(DetailView):
    model = Playlist
    template_name='playlist_detail.html'
    def get_context_data(self, **kwargs):
        context = super(PlaylistDetail, self).get_context_data(**kwargs)
        return context

class SongCreate(LoginRequiredMixin, CreateView):
    model = Song
    template_name = 'add_song.html'

    form_class = SongForm

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assignem l'usuari actual a la llista de reproducció
        return super(SongCreate, self).form_valid(form)


def add_song(request, pk):
    if request.method == 'POST':
        # Obtener los datos de la solicitud POST
        nombre_cancion = request.POST.get('nombre_cancion')
        nombre_artista = request.POST.get('nombre_artista')
        nombre_album = request.POST.get('nombre_album')

        # Obtener o crear el artista
        artista, _ = Artist.objects.get_or_create(name=nombre_artista)

        # Crear la canción y asociar el artista
        cancion = Song.objects.create(title=nombre_cancion, album=nombre_album)
        cancion.artists.add(artista)

        # Agregar la canción a la playlist
        playlist = Playlist.objects.get(pk=pk)
        playlist.songs.add(cancion)

        # Devolver una respuesta JSON
        return JsonResponse({'mensaje': 'Canción agregada a la playlist correctamente'})
    else:
        # Si la solicitud no es POST, devolver un error
        return JsonResponse({'error': 'Método no permitido'}, status=405)

