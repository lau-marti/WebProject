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
      | My Playlist | Some description  | Pop         |
    And I submit the playlist form
    Then I'm viewing the details page for playlist by "user"
    And There are 1 playlists


  #Scenario: Register just playlist name and description
   # Given I login as user "user" with password "password"
    #When I register playlist
     # | name        | description       |
      #| The Tavern  | The Tabern Songs  |
    #Then I'm viewing the details page for playlist by "user"
     # | name        | description       |
      #| The Tavern  | The Tabern Songs  |
    #And There are 1 restaurants

  #Scenario: Try to register playlist without logging in
   # Given I'm not logged in
    #When I register playlist
     # | name        | description      |
      #| The Tavern  | The Tavern Songs |
    #Then I'm redirected to the login form
    #And There are 0 playlists