from functools import reduce

from behave import *
import operator
from django.db.models import Q

use_step_matcher("parse")

@given('Exists playlist registered by "{username}"')
def step_impl(context, username):
    from django.contrib.auth.models import User
    user = User.objects.get(username=username)
    from web.models import Playlist, Genre
    for row in context.table:
        playlist = Playlist.objects.create(user=user, name=row['name'])
        for genre_name in row['genres'].split(','):
            genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
            playlist.genres.add(genre)

@when('I register playlist')
def step_impl(context):
    for row in context.table:
        context.browser.visit(context.get_url('web:playlist_create'))
        if context.browser.url == context.get_url('web:playlist_create'):
            form = context.browser.find_by_id('inputform')
            for heading in row.headings:
                context.browser.fill(heading, row[heading])
            form.find_by_value('Submit').first.click()

@then('There are {count:n} playlists')
def step_impl(context, count):
    from web.models import Playlist
    assert count == Playlist.objects.count()

@then('I\'m viewing the details page for playlist by "{username}"')
def step_impl(context, username):
    q_list = [Q((attribute, context.table.rows[0][attribute])) for attribute in context.table.headings]
    from django.contrib.auth.models import User
    q_list.append(Q(('user', User.objects.get(username=username))))
    from web.models import Playlist
    playlist = Playlist.objects.filter(reduce(operator.and_, q_list)).get()
    assert context.browser.url == context.get_url(playlist)

@when('I edit the playlist with name "{name}"')
def step_impl(context, name):
    from web.models import Playlist
    playlist = Playlist.objects.get(name=name)
    context.browser.visit(context.get_url('web:playlist_edit', playlist.pk))
    if context.browser.url == context.get_url('web:playlist_edit', playlist.pk)\
            and context.browser.find_by_css('.login-form'):
        form = context.browser.find_by_css('.login-form')
        for heading in context.table.headings:
            context.browser.fill(heading, context.table[0][heading])
        form.find_by_css('.genericButton').first.click()

@when(u'I click on the "Create a playlist" button')
def step_impl(context):
    # Hacer clic en el botón "Create a playlist"
    context.browser.find_by_css('.genericButton.large-button').first.click()

@when(u'I fill out the playlist form with')
def step_impl(context):
    for row in context.table:
        for heading in row.headings:
            if heading != 'genre':
                context.browser.fill(heading, row[heading])
        # Seleccionar el género deseado
        genre = row['genre']
        # Hacer clic en el género deseado en el formulario
        context.browser.find_option_by_text(genre).first.click()

@when(u'I submit the playlist form')
def step_impl(context):
    # Enviar el formulario
    context.browser.find_by_css('.genericButton[type="submit"]').first.click()

@then('I\'m on the details page for playlist by "{username}"')
def step_impl(context, username):
    from django.contrib.auth.models import User
    user = User.objects.get(username=username)
    from web.models import Playlist
    playlist = Playlist.objects.filter(user=user).first()

    assert context.browser.url == context.get_url(playlist)






