Feature: Search Playlists
  In order to find my playlists on the web
  As a registered user
  I want to search for my registered playlists

  Background: There is a registered user and a registered playlist
    Given Exists a user "user" with password "password"
    And Exists playlist registered by "user"
      | name            | date        | genres    |
      | The First       | 1970-01-01  | pop, rock |

Scenario: Search for an existing playlist
    Given I login as user "user" with password "password"
    When I search for the playlist with name "The First"
    Then The playlist with name "The First" should exist

Scenario: Search for a non-existing playlist
    Given I login as user "user" with password "password"
    When I search for the playlist with name "Nonexistent Playlist"
    Then The playlist with name "Nonexistent Playlist" should not exist
