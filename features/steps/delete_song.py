# features/steps/delete_song.py
from datetime import timedelta

from behave import *
from splinter import Browser

from web.models import Playlist, Song

use_step_matcher("parse")

from behave import given
from django.contrib.auth.models import User
from web.models import Playlist

@when('I delete the song "{song_title}" form playlist "{playlist_name}"')
def step_impl(context, song_title, playlist_name):
    from web.models import Playlist
    playlist = Playlist.objects.get(name=playlist_name)
    context.browser.visit(context.get_url('web:playlist_detail', playlist.id))
    context.browser.find_by_text("Delete").first.click()

@when('I delete the song "{song_title}" form playlist "{playlist_name}" directly')
def step_impl(context, song_title, playlist_name):
    from web.models import Playlist
    playlist = Playlist.objects.get(name=playlist_name)
    song = Song.objects.get(title=song_title)
    context.browser.visit(context.get_url('web:song_delete', playlist.id, song.id))

