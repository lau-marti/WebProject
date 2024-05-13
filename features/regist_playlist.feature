Feature: Register Playlist
  To register a playlist
  As a registered user
  I want to register the playlist, along with its name, description, and genre

  Background: There is a registered user
    Given Exists a user "user" with password "password"

  Scenario: Create a new playlist
    Given  I login as user "user" with password "password"
    When I click on the "Create a playlist" button
    And I fill out the playlist form with
      | name        | description       | genre       |
      | My Playlist | Some description  | pop         |
    And I submit the playlist form
    Then I'm on the details page for playlist by "user"
    And There are 1 playlists

  Scenario: Try to create a new playlist without login
    When I register playlist
      | name        | description       | genre       |
      | My Playlist | Some description  | pop         |
    Then I'm redirected to the login form
