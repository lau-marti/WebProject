from behave import *

use_step_matcher("parse")

@when('I view the details for playlist "{playlist_name}"')
def step_impl(context, playlist_name):
    from web.models import Playlist
    playlist = Playlist.objects.get(name=playlist_name)
    context.browser.visit(context.get_url('web:playlist_detail', playlist.pk))
@then("I'm viewing a playlist songs list containing")
def step_impl(context):
    song_links = context.browser.find_by_css('.Paragraf1')
    for i, row in enumerate(context.table):
        assert row['name'] == song_links[i].text

@step("The list contains {count:n} songs")
def step_impl(context, count):
    assert count == len(context.browser.find_by_css('.Paragraf1'))


@then("I'm viewing playlists details including")
def step_impl(context):
    for heading in context.table.headings:
        context.browser.is_text_present(context.table[0][heading])
