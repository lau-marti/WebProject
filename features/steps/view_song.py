import time

from behave import *
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


@when('I click on the song "{song_name}"')
def step_impl(context, song_name):
    song_link = context.browser.find_by_text(song_name)
    song_link.submit()
    time.sleep(10)


@then('I\'m viewing the details of a song')
def step_impl(context):
    for row in context.table:
        assert context.song.name == row['name']
        assert context.song.artist == row['artist']
        assert context.song.album == row['album']
        assert context.song.duration == row['duration']
        assert context.song.url == row['URL']
