# features/steps/delete_song.py
from datetime import timedelta

from behave import *
from splinter import Browser

from web.models import Playlist, Song

use_step_matcher("parse")

from behave import given
from django.contrib.auth.models import User
from web.models import Playlist


class UnwantedElementException(Exception):
    """Excepción lanzada cuando se encuentra un elemento no deseado."""

    def __init__(self, element_text):
        self.element_text = element_text
        super().__init__(f"Found an unwanted element with text: '{element_text}'")


@given('Create a user "{username}" with password "{password}"')
def create_user(context, username, password):
    # Crear un nuevo usuario
    context.user = User.objects.create_user(username=username, email='', password=password)


@given('Create playlist "{playlist_name}" registered by "{username}"')
def create_playlist(context, playlist_name, username):
    # Buscar al usuario por nombre de usuario
    user = User.objects.get(username=username)

    # Crear una lista de reproducción para el usuario
    playlist = Playlist.objects.create(user=user, name=playlist_name)

    # Agregar la lista de reproducción al contexto para que esté disponible en otros pasos
    context.playlist = playlist

@given('Playlist "{playlist_song}" registered by "{user}" contains the songs')
def add_songs_to_playlist(context, playlist_song, user):
    # Código para agregar canciones a la lista de reproducción en la base de datos de prueba
    for row in context.table:
        title = row["song_title"]
        album = row["album"]
        duration_str = row["duration"]
        duration_parts = duration_str.split(":")
        duration = timedelta(
            hours=int(duration_parts[0]),
            minutes=int(duration_parts[1]),
            seconds=int(duration_parts[2])
        )
        song = Song.objects.create(
            title=title,
            album=album,
            duration=duration
        )
        context.playlist.songs.add(song)


@given('User "{username}" login with password "{password}"')
def step_impl(context, username, password):
    context.browser.visit(context.get_url('/accounts/login/?next=/musicterritory/'))
    form = context.browser.find_by_id('loginform')
    context.browser.fill('username', username)
    context.browser.fill('password', password)
    form.find_by_id('submitlogin').first.click()
    assert context.browser.is_text_present('Hi ' + username + '!')


@when('I delete a song with name "{song_name}" from the playlist')
def delete_song(context, song_name):
    # Encontrar el elemento que contiene el texto del nombre de la canción y hacer clic en él
    context.browser.find_by_text(song_name).first.click()


@then('the playlist should contain 1 fewer song')
def verify_playlist_song_count(context):
    # Verificar que la cantidad de canciones en la lista de reproducción ha disminuido en 1
    initial_song_count = len(context.playlist.songs.all())
    context.browser.reload()  # Recargar la página para actualizar la lista de canciones
    final_song_count = len(context.browser.find_by_css('.cançons li'))
    assert initial_song_count - 1 == final_song_count


@given('I remember the number of songs in the playlist')
def remember_song_count(context):
    context.initial_song_count = len(context.playlist.songs.all())


@given('I go to the playlist detail page for "{playlist_name}"')
def go_to_playlist_details(context, playlist_name):
    context.browser.find_by_text(playlist_name).first.click()


@when('I try to delete song with name "{song_name}" from the playlist makes exception')
def delete_song_exception(context, song_name):
    try:
        button = context.browser.find_by_text(song_name).first
        if button:
            raise UnwantedElementException(song_name)
    except UnwantedElementException as e:
        print(e)
