from django import forms
from .models import Playlist, Song

class PlaylistForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'no-resize'}))

    class Meta:
        model = Playlist
        exclude = ('user', 'songs', 'date')

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude = ('user', 'playlist', 'name', 'artists')
