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
    user = User.objects.get(username=username)
    from web.models import Playlist
    playlist = Playlist.objects.get(name=playlist_name)
    from web.models import Song
    for row in context.table:
        song = Song(playlist=playlist, user=user)
        for heading in row.headings:
            setattr(song, heading, row[heading])
        song.save()

@when('I register song at playlist "{playlist_name}"')
def step_impl(context, playlist_name):
    from web.models import Playlist
    playlist = Playlist.objects.get(name=playlist_name)
    for row in context.table:
        context.browser.visit(context.get_url('web:song_create', playlist.pk))
        if context.browser.url == context.get_url('web:song_create', playlist.pk):
            form = context.browser.find_by_id('input-form').first
            for heading in row.headings:
                if heading == 'image':
                    filePath = os.path.join(BASE_DIR, row[heading])
                    context.browser.fill(heading, filePath)
                else:
                    context.browser.fill(heading, row[heading])
            form.find_by_value('Submit').first.click()

@then('I\'m viewing the details page for song at playlist "{playlist_name}" by "{username}"')
def step_impl(context, playlist_name, username):
    q_list = [Q((attribute, context.table.rows[0][attribute])) for attribute in context.table.headings]
    from django.contrib.auth.models import User
    q_list.append(Q(('user', User.objects.get(username=username))))
    from web.models import Playlist
    q_list.append(Q(('restaurant', Playlist.objects.get(name=playlist_name))))
    from web.models import Song
    song = Song.objects.filter(reduce(operator.and_, q_list)).get()
    assert context.browser.url == context.get_url(song)
    if song.image:
        song.image.delete()

@then('There are {count:n} songs')
def step_impl(context, count):
    from web.models import Song
    assert count == Song.objects.count()

