Feature: View Playlist
  In order to know about a playlist
  As a user
  I want to view the playlist details including all its songs

  Background: There is one playlist with 2 songs and another without
    Given Exists a user "user1" with password "password"
    And Exists a user "user2" with password "password"
    And Exists playlist registered by "user1"
      | name            | description         | date          | genres      |
      | Famous          | Form singer Famous  | 2023-05-23    | pop, rock   |
      | Unknown         |                     | 2002-o6-09    | alternative |
    And Exists song at playlist "Famous" by "user1"
      | name            |
      | Fish and Chips  |
    And Exists song at playlist "Unknown" by "user1"
      | name            |
      | Apple Pie       |

  Scenario: View details for owned playlist with songs
    Given I login as user "user1" with password "password"
    When I view the details for playlist "Famous"
    Then I'm viewing playlists details including
      | name            | description         | date          | genres      |
      | Famous          | Form singer Famous  | 2023-05-23    | pop, rock   |
    And There is "Editar Playlist" link available
    And There is "Afegir Cançó" link available
    And I'm viewing a playlist songs list containing
      | name            |
      | Fish and Chips  |
      | Apple Pie       |
    And The list contains 2 songs

  Scenario: View details for other user playlist with no songs
    Given I login as user "user2" with password "password"
    When I view the details for playlist "Unknown"
    Then I'm viewing playlists details including
      | name            | description         | date          | genres      |
      | Unknown         |                     | 2002-o6-09    | alternative |
    And There is no "Editar Playlist" link available
    And There is no "Afegir Cançó" link available
    And I'm viewing a playlist songs list containing
      | name            |
    And The list contains 0 songs
