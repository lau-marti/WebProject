from django.core.exceptions import PermissionDenied
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView,  ListView
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

class PlaylistList(ListView):
    model = Playlist
    template_name = 'home.html'
    context_object_name = 'all_playlists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_playlists'] = self.request.user.playlist_set.all()
        return context

class DeletePlaylist(DeleteView):
    model = Playlist
    template_name = 'playlist_confirm_delete.html'  # Plantilla para confirmar la eliminación
    success_url = reverse_lazy('web:playlist_list')  # URL a la que se redireccionará después de la eliminación

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

class SongCreate(CreateView):
    model = Song
    fields = ['title', 'album', 'artists']
    template_name = 'add_song.html'  # Plantilla para el formulario de creación
    success_url = 'playlist_list' # Redirige después de agregar la canción a la playlist

    def post(self, request, *args, **kwargs):
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

            # Obtener la playlist y agregar la canción
            playlist_pk = self.kwargs['pk']
            playlist = Playlist.objects.get(pk=playlist_pk)
            playlist.songs.add(cancion)

            # Devolver una respuesta JSON
            return JsonResponse({'mensaje': 'Canción agregada a la playlist correctamente'})
        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405)


class SongDelete(DeleteView):
    model = Song
    def post(self, request, *args, **kwargs):
        # Obtener la instancia de la lista de reproducción
        playlist = get_object_or_404(Playlist, pk=self.kwargs['pk'])
        # Obtener la instancia de la canción que se desea eliminar
        song = get_object_or_404(Song, pk=self.kwargs['pkr'])
        # Eliminar la canción de la lista de reproducción
        playlist.songs.remove(song)
        # Guardar los cambios
        playlist.save()
        song.delete()
        # Redirigir a la página de detalles de la lista de reproducción
        return redirect('web:playlist_detail', pk=playlist.id)
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
        playlist_detail_url = reverse('playlist_detail', args=[pk])

        # Devolver una respuesta JSON
        return JsonResponse({'mensaje': 'Canción agregada a la playlist correctamente'})
    else:
        # Si la solicitud no es POST, devolver un error
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def delete_song(request, song_id, playlist_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        song = get_object_or_404(Song, id=song_id)
        playlist.songs.remove(song)
        return redirect(playlist.get_absolute_url())
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def search_playlists(request):
    query = request.GET.get('searchValue', '')
    playlists = Playlist.objects.filter(name__icontains=query)
    results = [{'id': playlist.id, 'name': playlist.name, 'user': playlist.user.username} for playlist in playlists]
    return JsonResponse({'playlists': results}, safe=False)
