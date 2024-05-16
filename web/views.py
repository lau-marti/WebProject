from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView,  ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import PlaylistForm, SongForm
from .models import Playlist, Song, Artist
from django.contrib.auth.decorators import login_required
from datetime import timedelta

class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class CheckIsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        playlist_pk = self.kwargs.get('pk')
        playlist = Playlist.objects.get(pk=playlist_pk)
        if not playlist.user == self.request.user:
            raise PermissionDenied("No tienes permiso para acceder a este recurso.")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.user == self.request.user:
            raise PermissionDenied("No tienes permiso para acceder a este recurso.")
        return obj


class LoginRequiredCheckIsOwnerUpdateView(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
    template_name ='form.html'


class PlaylistList(ListView):
    model = Playlist
    template_name = 'home.html'
    context_object_name = 'all_playlists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_playlists'] = self.request.user.playlist_set.all()
        return context

class DeletePlaylist(LoginRequiredMixin,CheckIsOwnerMixin, DeleteView):
    model = Playlist
    template_name = 'playlist_confirm_delete.html'  # Plantilla para confirmar la eliminación
    success_url = reverse_lazy('web:playlist_list')  # URL a la que se redireccionará después de la eliminación

    def delete(self, request, *args, **kwargs):
        playlist = self.get_object()

        # Obtener todas las canciones asociadas a la playlist
        songs = playlist.songs.all()

        # Eliminar las canciones asociadas solo a esta playlist
        for song in songs:
            if playlist in song.songs_to_playlist.all():
                song.delete()

        # Luego de eliminar las canciones asociadas, eliminar la playlist
        response = super().delete(request, *args, **kwargs)

        # Verificar si alguna de las canciones eliminadas no está referenciada por ninguna otra playlist
        for song in songs:
            if not Playlist.objects.filter(songs=song).exists():
                song.delete()

        return response

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


class SongCreate(LoginRequiredMixin,CheckIsOwnerMixin, CreateView):
    model = Song
    fields = ['title', 'album', 'artists']
    template_name = 'add_song.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Obtener los datos de la solicitud POST
            nombre_cancion = request.POST.get('nombre_cancion')
            nombre_artista = request.POST.get('nombre_artista')
            nombre_album = request.POST.get('nombre_album')
            url_imagen = request.POST.get('url_imagen')
            duracion_str = request.POST.get('duracion')  # Obtener la duración como cadena
            url_cancion = request.POST.get('url_cancion')  # Obtener la URL de la canción

            # Convertir la duración a timedelta
            if duracion_str:
                minutos, segundos = map(int, duracion_str.split(':'))
                duracion_total_segundos = minutos * 60 + segundos
                duracion_timedelta = timedelta(seconds=duracion_total_segundos)
            else:
                duracion_timedelta = None

            with transaction.atomic():
                # Verificar si la canción ya existe
                cancion_existente = Song.objects.filter(title=nombre_cancion, artists__name=nombre_artista).first()

                if cancion_existente:
                    # Si la canción ya existe, no es necesario crear una nueva
                    playlist_pk = self.kwargs['pk']
                    playlist = Playlist.objects.get(pk=playlist_pk)
                    playlist.songs.add(cancion_existente)
                    return JsonResponse({'mensaje': 'Canción ya existente agregada a la playlist correctamente'})
                else:
                    # Si la canción no existe, crearla y asociarla al artista
                    artista, _ = Artist.objects.get_or_create(name=nombre_artista)
                    cancion = Song.objects.create(title=nombre_cancion, album=nombre_album, duration=duracion_timedelta,
                                                  url_imagen=url_imagen, url_cancion=url_cancion)
                    cancion.artists.add(artista)
                    playlist_pk = self.kwargs['pk']
                    playlist = Playlist.objects.get(pk=playlist_pk)
                    playlist.songs.add(cancion)
                    return JsonResponse({'mensaje': 'Canción agregada a la playlist correctamente'})
        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405)
class SongDelete( LoginRequiredMixin, CheckIsOwnerMixin, DeleteView):
    model = Song

    def post(self, request, *args, **kwargs):
        # Obtener la instancia de la lista de reproducción
        playlist = get_object_or_404(Playlist, pk=self.kwargs['pk'])
        # Obtener la instancia de la canción que se desea eliminar
        song = get_object_or_404(Song, pk=self.kwargs['pkr'])

        # Verificar si hay otras listas de reproducción que contienen esta canción
        other_playlists_with_song = Playlist.objects.filter(songs=song).exclude(pk=playlist.pk)

        # Si no hay otras listas de reproducción que contienen esta canción, eliminarla
        if not other_playlists_with_song.exists():
            song.delete()

        # Eliminar la canción de la lista de reproducción actual
        playlist.songs.remove(song)
        # Guardar los cambios en la lista de reproducción
        playlist.save()

        # Redirigir a la página de detalles de la lista de reproducción
        return redirect('web:playlist_detail', pk=playlist.id)

# def add_song(request, pk):
#     if request.method == 'POST':
#         # Obtener los datos de la solicitud POST
#         nombre_cancion = request.POST.get('nombre_cancion')
#         nombre_artista = request.POST.get('nombre_artista')
#         nombre_album = request.POST.get('nombre_album')
#
#         # Obtener o crear el artista
#         artista, _ = Artist.objects.get_or_create(name=nombre_artista)
#
#         # Crear la canción y asociar el artista
#         cancion = Song.objects.create(title=nombre_cancion, album=nombre_album)
#         cancion.artists.add(artista)
#
#         # Agregar la canción a la playlist
#         playlist = Playlist.objects.get(pk=pk)
#         playlist.songs.add(cancion)
#         playlist_detail_url = reverse('playlist_detail', args=[pk])
#
#         # Devolver una respuesta JSON
#         return JsonResponse({'mensaje': 'Canción agregada a la playlist correctamente'})
#     else:
#         # Si la solicitud no es POST, devolver un error
#         return JsonResponse({'error': 'Método no permitido'}, status=405)

# def delete_song(request, song_id, playlist_id):
#     if request.method == 'POST':
#         playlist = get_object_or_404(Playlist, pk=playlist_id)
#         song = get_object_or_404(Song, id=song_id)
#         playlist.songs.remove(song)
#         return redirect(playlist.get_absolute_url())
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)


def search_playlists(request):
    query = request.GET.get('searchValue', '')
    playlists = Playlist.objects.filter(name__icontains=query)
    results = [{'id': playlist.id, 'name': playlist.name, 'user': playlist.user.username} for playlist in playlists]
    return JsonResponse({'playlists': results}, safe=False)


class SongDetailView(DetailView):
    model = Song
    template_name = 'song_detail.html'  # Nombre de la plantilla que mostrará la información detallada de la canción
    context_object_name = 'song'  # Nombre del objeto de contexto que contendrá la información de la canción en la plantilla

