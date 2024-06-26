import time
from datetime import timedelta

from behave import *
from django.contrib.auth.models import User

from web.models import Playlist, Song

use_step_matcher("parse")


@step('I click on the button with name "{playlist_name}"')
def step_impl(context, playlist_name):
    button = context.browser.find_by_css(".playlistButton")
    button.click()
@step('I register a song at playlist "{playlist_name}"')
def step_impl(context, playlist_name):
    add_song_button = context.browser.find_by_css(".genericButton.addSongButton")
    add_song_button.click()
    search_box = context.browser.find_by_id("searchInput")
    search_box.fill("never gonna give you up")
    search_button = context.browser.find_by_css(".genericButton.searchButton")
    search_button.click()
    add_button = context.browser.find_by_css(".genericButton.addButton")
    add_button.click()


@then('I click on the song "{song_name}"')
def step_impl(context, song_name):
    context.browser.find_by_text(song_name).first.click()

@then('I\'m viewing the details of "{song_name}"')
def step_impl(context, song_name):
    from web.models import Song
    song = Song.objects.get(title=song_name)
    context.browser.url.endswith("/songs/"+str(song.id))

@given('Playlist "{playlist_song}" registered by "{user}" contains the songs')
def add_songs_to_playlist(context, playlist_song, user):
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

@given('Create playlist "{playlist_name}" registered by "{username}"')
def create_playlist(context, playlist_name, username):
    user = User.objects.get(username=username)

    playlist = Playlist.objects.create(user=user, name=playlist_name)

    context.playlist=playlist