from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import UpdateView, DeleteView
from .models import Playlist, Song
from django.contrib.auth.decorators import login_required

@login_required
def create_playlist(request):
    if request.method == 'POST':
        name = request.POST['name']
        songs = request.POST.getlist('songs')
        playlist = Playlist(user=request.user, name=name)
        playlist.save()
        playlist.songs.add(*songs)
        return redirect('playlist_detail', playlist_id=playlist.id)
    else:
        return render(request, 'create_playlist.html')