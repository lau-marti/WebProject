from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse


# This is an example of a model in Django so that you can see how you can define your own models :D
# DON'T FORGET to run `python manage.py makemigrations` and `python manage.py migrate` after changing this file!!!
class Song(models.Model):
    title = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    duration = models.DurationField(null=True)
    lyrics = models.TextField(null=True)
    artists = models.ManyToManyField('Artist', related_name='artists_to_song')
    genre = models.ManyToManyField('Genre', related_name='genres_to_song')

    def __unicode__(self):
        return u"%s" % self.title

    def get_absolute_url(self):
        return reverse('web:song_detail.html', kwargs={'pkr': self.song.pk, 'pk': self.pk})


class Artist(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    monthly_listeners = models.IntegerField(null=True)
    #songs = models.ManyToManyField('Song', related_name='songs_to_artist')
    genres = models.ManyToManyField('Genre', related_name='genres_to_artist')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    #songs = models.ManyToManyField('Song', related_name='songs_to_genre')
    #artists = models.ManyToManyField('Artist', related_name='artists_to_genre')

    def __str__(self):
        return self.name

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Si es borra l'usuari, també les seves playlist
    name = models.CharField(max_length=100)
    date = models.DateField(default=date.today)
    description = models.TextField(null=True)
    genres = models.ManyToManyField(Genre, related_name='genres_to_playlist')
    songs = models.ManyToManyField(Song, related_name='songs_to_playlist')

    def __unicode__(self):
        return u"%s" % self.name

    def get_absolute_url(self):
        return reverse('web:playlist_detail', kwargs={'pk': self.pk})
