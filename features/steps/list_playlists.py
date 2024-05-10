from behave import *

use_step_matcher("parse")

@when('I list playlists')
def step_impl(context):
    context.browser.visit(context.get_url('web:playlist_list'))

@then('I\'m viewing a list containing my playlists')
def step_impl(context):
    playlist_links = context.browser.find_by_css('.playlistButton.myplaylists')
    for i, row in enumerate(context.table):
        assert row['name'] == playlist_links[i].text
@then('I\'m viewing a list containing all playlists')
def step_impl(context):
    playlist_links = context.browser.find_by_css('.playlistButton.allplaylists')
    for i, row in enumerate(context.table):
        assert row['name'] == playlist_links[i].text

@step('The list contains {count:n} playlists (all)')
def step_impl(context, count):
    assert count == len(context.browser.find_by_css('.playlistButton.allplaylists'))

@step('The list contains {count:n} playlists (my)')
def step_impl(context, count):
    assert count == len(context.browser.find_by_css('.playlistButton.myplaylists'))

