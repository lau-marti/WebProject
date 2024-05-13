Feature: List Playlists
  In order to keep myself up to date about playlists registered in web
  As a registered user
  I want to list the last registered playlists

  Background: There is a registered user and 1 registered playlists
    Given Exists a user "user" with password "password"
    And Exists playlist registered by "user"
      | name        | date        | genres    |
      | PlayList1   | 2014-05-13  | pop       |
    And I login as user "user" with password "password"
    And I click on the button with name "PlayList1"
    And I register a song at playlist "PlayList1"
      | name                     |
      | Never Gonna Give You Up  |

  Scenario: Vew song Information
    Given I login as user "user" with password "password"
    When I click on the button with name "PlayList1"
    And I click on the song "Never Gonna Give You Up"
      | name                     |
      | Never Gonna Give You Up  |
    Then I'm viewing the details of a song
      | name                     | artist      | album                      | duration | URL                                         |
      | Never Gonna Give You Up  | Rick Astley | Whenever You Need Somebody | 3:33     | https://www.youtube.com/watch?v=dQw4w9WgXcQ |