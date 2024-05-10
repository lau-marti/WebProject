Feature: LogOut
  To logout
  As a registered user


  Scenario: # Enter scenario name here
    # Enter steps here



Feature: Register Playlist
  To register a playlist
  As a registered user
  I want to register the playlist, along with its name, description, and genre

  Background: There is a registered user
    Given Exists a user "user" with password "password"
    And I login as user "user" with password "password"

  Scenario: Create a new playlist
    When I click on the "Create a playlist" button
    And I fill out the playlist form with:
      | name        | description       | genre       |
      | My Playlist | Some description  | pop         |
    And I submit the playlist form
    Then I'm on the details page for playlist by "user"
    And There are 1 playlists