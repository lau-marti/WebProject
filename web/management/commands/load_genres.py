from django.core.management.base import BaseCommand
from web.models import Genre
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Command(BaseCommand):
    help = 'Carga los géneros de música desde Spotify y los guarda en un archivo de texto'

    def handle(self, *args, **kwargs):
        # Tu código para cargar los géneros de música y guardarlos en el archivo de texto
        client_id = '7f44fa05891c4b0388022a3317aea4cb'
        client_secret = '3f2c3b851b4a4973b44ae04c7bbaf4b7'
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        generos_spotify = sp.recommendation_genre_seeds()

        for genero in generos_spotify['genres']:
            Genre.objects.get_or_create(name=genero)