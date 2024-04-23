
from django.forms import ModelForm
from .models import Playlist, Song


class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        exclude = ('user','songs',)


class SongForm(ModelForm):
    class Meta:
        model = Song
        exclude = ('user','playlist',)
