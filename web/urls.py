from django.urls import path
from django.utils import timezone
from django.views.generic import DetailView, ListView
from web.forms import PlaylistForm
from web.views import PlaylistCreate, PlaylistDetail, LoginRequiredCheckIsOwnerUpdateView, SongCreate, add_song
from web.models import Song, Playlist


app_name = "web"

urlpatterns = [
    path('',
         ListView.as_view(
             queryset=Playlist.objects.filter(date__lte=timezone.now()).order_by('-date')[:5],
             context_object_name='latest_playlist_list',
             template_name='home.html'),
         name='playlist_list'),


    #Playlist details, ex.: /playlists/1/
    path('playlists/<int:pk>',
         PlaylistDetail.as_view(),
         name='playlist_detail'),

    #Playlist song details, ex: /songs/1/
    path('songs/<int:pk>',
         DetailView.as_view(
             model=Song,
             template_name = 'song_detail.html'),
         name='song_detail'),

    #Create a playlist, /playlists/create/
    path('playlists/create',
         PlaylistCreate.as_view(),
         name='playlist_create'),

    #Edit playlist details, ex.: /playlists/1/edit/
    path('playlists/<int:pk>/edit',
        LoginRequiredCheckIsOwnerUpdateView.as_view(
            model=Playlist,
            form_class=PlaylistForm),
        name='playlist_edit'),

    # Create a playlist, ex.: /musicterritory/playlists/1/songs/create/
    path('playlists/<int:pk>/songs/create',
        SongCreate.as_view(),
        name='song_create'),

    path('playlists/<int:pk>/songs/add_song', add_song, name='add_song'),

    ]