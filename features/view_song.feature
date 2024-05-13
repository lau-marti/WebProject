Feature: List Playlists
  In order to keep myself up to date about playlists registered in web
  As a registered user
  I want to list the last registered playlists

  Background: There is a registered user and 1 registered playlists
    Given Exists a user "user" with password "password"
    And Create playlist "The First" registered by "user"
      | name      | date       | genres    |
      | PlayList1 | 1970-01-01 | pop, rock |
    And Playlist "The First" registered by "user" contains the songs
      | song_title | album | duration |
      | Never Gonna Give You Up | Whenever You Need Somebody | 00:04:30 |
    And I login as user "user" with password "password"
    And I click on the button with name "PlayList1"


  Scenario: Vew song Information
    Then I click on the song "Never Gonna Give You Up"
      | name                     |
      | Never Gonna Give You Up  |
    Then I'm viewing the details of "Never Gonna Give You Up"
