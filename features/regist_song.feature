Feature: Register Song
  In order to keep track of the dishes I eat
  As a user
  I want to register a dish in the corresponding restaurant together with its details

  Background: There is a registered user and restaurant
    Given Exists a user "user" with password "password"
    And Exists a user "user1" with password "password"
    And Exists playlist registered by "user"
      | name            | description         | date          | genres      |
      | Famous          | Form singer Famous  | 2023-05-23    | pop, rock   |
    And Exists playlist registered by "user"
      | name            | description         | date          | genres      |
      | Unknown         |                     | 2003-08-25    | pop         |

  Scenario: Register a song to a playlist
    Given I login as user "user" with password "password"
    When I view the details for playlist "Famous"
    And I search and add song "Hello" to playlist "Famous"
    Then I'm viewing a playlist songs list containing
      | name     |
      | Hello    |
    And The list contains 1 songs
    And There are 1 songs

  Scenario: Register two songs to diferent playlists.
    Given I login as user "user1" with password "password"
    And Exists song at playlist "Famous" by "user"
      | name     |album   | artists |
      | Hello    |25      | Adele, Pepito    |
    When I view the details for playlist "Unknown"
    And I search and add song "Hello" to playlist "Unknown"
    Then I'm viewing a playlist songs list containing
      | name     |
      | Hello    |
    And The list contains 1 songs
    And There are 2 songs

