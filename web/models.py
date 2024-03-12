from django.db import models

# This is an example of a model in Django so that you can see how you can define your own models :D
# DON'T FORGET to run `python manage.py makemigrations` and `python manage.py migrate` after changing this file!!!
class Song(models.Model):
    title = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    duration = models.DurationField()
    lyrics = models.TextField()
    artists = models.ManyToManyField('Artist', on_delete=models.CASCADE)
    genre = models.ManyToManyField('Genre')
    def __str__(self):
        return self.title
class Artist(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    monthly_listeners = models.IntegerField()
    songs = models.ManyToManyField('Song')
    genres = models.ManyToManyField('Genre')
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField('Song')
    artists = models.ManyToManyField('Artist', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
