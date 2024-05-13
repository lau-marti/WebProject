Feature: Edit Playlist
  In order to keep updated my previous registers about playlists
  As a user
  I want to edit a playlist register I created

  Background: There are registered users and a playlists by one of them
    Given Exists a user "user1" with password "password"
    And Exists a user "user2" with password "password"
    And Exists playlist registered by "user1"
      | name      | description              | genres        |
      | Hits      | New spanish Hits         | pop           |

  Scenario: Edit owned playlist registry description
    Given I login as user "user1" with password "password"
    When I edit the playlist with name "Hits"
      | description        |
      | New american Hits  |
    Then I'm viewing the details page for playlist by "user1"
      | name     | description            | genres        |
      | Hits     | New american Hits      | pop           |
    And There are 1 playlists

  Scenario: Try to edit playlist and the owner edit button
    Given I login as user "user1" with password "password"
    When I view the details for playlist "Hits"
    Then There is "Edit Playlist" link available

  Scenario: Try to edit playlist but not the owner no edit button
    Given I login as user "user2" with password "password"
    When I view the details for playlist "Hits"
    Then There is no "Edit Playlist" link available

  Scenario: Force edit playlist but not the owner permission exception
    Given I login as user "user2" with password "password"
    When I edit the playlist with name "Hits"
      | description         |
      | New american Hits   |
    Then Server responds with page containing "403 Forbidden"