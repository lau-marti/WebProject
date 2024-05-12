from behave import *

use_step_matcher("parse")

@when('I search for the playlist with name "{name}"')
def step_when_search_for_playlist(context, name):
    context.browser.visit(context.get_url('web:playlist_list'))
    search_box = context.browser.find_by_css('.search-input')
    search_box.fill(name)
    search_button = context.browser.find_by_css('.genericButton')
    search_button.click()

@step('The playlist with name "{name}" should exist')
def step_then_playlist_should_exist(context, name):
    playlist_links = context.browser.find_by_css('.playlistButton')
    for link in playlist_links:
        if name in link.text:
            return
    assert False, f'No se encontró la playlist con nombre "{name}"'

@step('The playlist with name "{name}" should not exist')
def step_then_playlist_should_not_exist(context, name):
    playlist_links = context.browser.find_by_css('.playlistButton')
    for link in playlist_links:
        if name in link.text:
            assert False, f'Se encontró la playlist con nombre "{name}"'
