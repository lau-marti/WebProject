from django.core.management.base import BaseCommand
from web.models import Genre
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Command(BaseCommand):
    help = 'Carga los géneros de música desde Spotify y los guarda en un archivo de texto'

    def handle(self, *args, **kwargs):
        # Tu código para cargar los géneros de música y guardarlos en el archivo de texto
        generos_spotify = [
            "world-music", "work-out", "turkish", "trip-hop", "trance", "techno", "tango", "synth-pop", "swedish", "summer",
            "study", "spanish", "soundtracks", "soul", "songwriter", "sleep", "ska", "singer-songwriter", "show-tunes",
            "sertanejo", "samba", "salsa", "sad", "romance", "rockabilly", "rock-n-roll", "rock", "road-trip", "reggaeton",
            "reggae", "rainy-day", "r-n-b", "punk-rock", "punk", "psych-rock", "progressive-house", "power-pop", "post-dubstep",
            "pop-film", "pop", "piano", "philippines-opm", "party", "pagode", "opera", "new-release", "new-age", "mpb",
            "movies", "minimal-techno", "metalcore", "metal-misc", "metal", "mandopop", "malay", "latino", "latin", "kids",
            "k-pop", "jazz", "j-rock", "j-pop", "j-idol", "j-dance", "iranian", "industrial", "indie-pop", "indie", "indian",
            "idm", "house", "honky-tonk", "holidays", "hip-hop", "heavy-metal", "hardstyle", "hardcore", "hard-rock", "happy",
            "guitar", "grunge", "groove", "grindcore", "goth", "gospel", "german", "garage", "funk", "french", "forro", "folk",
            "emo", "electronic", "electro", "edm", "dubstep", "dub", "drum-and-bass", "disney", "disco", "detroit-techno",
            "deep-house", "death-metal", "dancehall", "dance", "country", "comedy", "club", "classical", "chill", "children",
            "chicago-house", "cantopop", "british", "breakbeat", "brazil", "bossanova", "blues", "bluegrass", "black-metal",
            "anime", "ambient", "alternative", "alt-rock", "afrobeat", "acoustic"
        ]

        for genero in generos_spotify:
            Genre.objects.get_or_create(name=genero)
