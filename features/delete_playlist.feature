Feature: Delete Playlists
  In order to manage my playlists in the web
  As a registered user
  I want to delete my registered playlists

  Background: There is a registered user and a registered playlist
    Given Exists a user "user" with password "password"
    Given Exists a user "user1" with password "password1"
    And Exists playlist registered by "user"
      | name            | date        | genres    |
      | The First       | 1970-01-01  | pop, rock |

  Scenario: Delete my playlist
    Given I login as user "user" with password "password"
    When I delete the playlist with name "The First"
    Then The playlist with name "The First" should not exist

  Scenario: Cannot  delete another user's playlist
    Given I login as user "user1" with password "password1"
    When I attempt to delete the playlist with name "The First"
    Then The playlist with name "The First" should still exist
    
  Scenario: Try to delete another user's playlist
    Given I login as user "user1" with password "password1"
    When I delete the playlist with name "The First"
    Then Server responds with page containing "403 Forbidden"
