from behave import *
import time

use_step_matcher("parse")

@when('I delete the playlist with name "{name}"')
def step_when_i_delete_the_playlist(context, name):
    delete_button = context.browser.find_by_css('.deleteButton')
    delete_button.click()

@then('The playlist with name "{name}" should not exist')
def step_then_the_playlist_should_not_exist(context, name):

    context.browser.visit(context.get_url('web:playlist_list'))

    playlist_elements = context.browser.find_by_css('.playlistButton .myplaylists')
    playlist_pks = [el.get_attribute('data-pk') for el in playlist_elements]
    assert name not in playlist_pks, f'La playlist con pk "{name}" todavía existe'


@when('I attempt to delete the playlist with name "{name}"')
def step_when_i_attempt_to_delete_the_playlist(context, name):
    from web.models import Playlist

    playlist = Playlist.objects.get(name=name)
    url_actual = context.browser.url
    context.browser.visit(url_actual + 'playlists/'+str(playlist.pk)+'/delete')

@step('The playlist with name "{name}" should still exist')
def step_then_playlist_should_still_exist(context, name):
    context.browser.visit(context.get_url('web:playlist_list'))

    playlist_links = context.browser.find_by_css('a.playlistButton.allplaylists')
    for link in playlist_links:
        if name in link.text:
            assert True, f'La playlist con nombre "{name}" todavía existe. El test ha pasado correctamente.'
            break
    else:
        assert False, f'No se encontró la playlist con nombre "{name}"'