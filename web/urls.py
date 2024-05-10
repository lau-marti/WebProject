from django.urls import path, include
from django.utils import timezone
from django.views.generic import DetailView, ListView

from web import views
from web.forms import PlaylistForm
from web.views import PlaylistCreate, PlaylistDetail, LoginRequiredCheckIsOwnerUpdateView, SongCreate, add_song, delete_song, PlaylistList, DeletePlaylist, SongDelete, search_playlists
from web.models import Song, Playlist

app_name = "web"

urlpatterns = [

    path('',
         PlaylistList.as_view(),
         name='playlist_list'),

    path('playlists/<int:pk>/delete',
         DeletePlaylist.as_view(),
         name='playlist_delete'),

    #Playlist details, ex.: /playlists/1/
    path('playlists/<int:pk>/',
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

    path('playlists/<int:pk>/songs/<int:pkr>/delete',
         SongDelete.as_view(),
         name='song_delete'),

    path('search_playlists/', search_playlists, name='search_playlists'),

    path('songs/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),


]