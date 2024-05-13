import time
from functools import reduce

from behave import *
import operator
from django.db.models import Q
import os

from project.settings import BASE_DIR

use_step_matcher("parse")


@given('Exists song at playlist "{playlist_name}" by "{username}"')
def step_impl(context, playlist_name, username):
    from django.contrib.auth.models import User
    from web.models import Playlist, Song, Artist

    user = User.objects.get(username=username)
    playlist = Playlist.objects.get(name=playlist_name)

    for row in context.table:
        song = Song.objects.create(title=row['name'])
        # Asignación de valores a las columnas presentes en la tabla
        if 'album' in row.headings:
            song.album = row['album']
        if 'duration' in row.headings:
            song.duration = row['duration']
        if 'URL' in row.headings:
            song.URL = row['URL']
        if 'artists' in row.headings:
            for artist_name in row['artists'].split(','):
                artist, _ = Artist.objects.get_or_create(name=artist_name.strip())
                song.artists.add(artist)

        song.save()
        playlist.songs.add(song)


@when('I search and add song "{song_title}" to playlist "{playlist_name}"')
def step_impl(context, song_title, playlist_name):
    from web.models import Playlist
    playlist = Playlist.objects.get(name=playlist_name)
    context.browser.visit(context.get_url('web:song_create', playlist.pk))
    if context.browser.url == context.get_url('web:song_create', playlist.pk):
        context.browser.fill('search', song_title)
        context.browser.find_by_css('div#content button').click()
        # Select the song from the search results
        search_results = context.browser.find_by_id('searchResults')
        time.sleep(2)
        context.browser.find_by_id('add_0').click()
        time.sleep(2)




@then('I\'m viewing the details page for song at playlist "{playlist_name}" by "{username}"')
def step_impl(context, playlist_name, username):
    q_list = [Q((attribute, context.table.rows[0][attribute])) for attribute in context.table.headings]
    from django.contrib.auth.models import User
    q_list.append(Q(('user', User.objects.get(username=username))))
    from web.models import Playlist
    q_list.append(Q(('playlist', Playlist.objects.get(name=playlist_name))))
    from web.models import Song
    song = Song.objects.filter(reduce(operator.and_, q_list)).get()
    assert context.browser.url == context.get_url(song)
    if song.image:
        song.image.delete()


@then('There are {count:n} songs')
def step_impl(context, count):
    from web.models import Song
    assert count == Song.objects.count()

