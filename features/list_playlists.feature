Feature: List Playlists
  In order to keep myself up to date about playlists registered in web
  As a registered user
  I want to list the last 5 registered playlists

  Background: There is a registered user and 5 registered playlists by diferent users
    Given Exists a user "user" with password "password"
    And Exists a user "user1" with password "password"
    And Exists playlist registered by "user"
      | name            | date        | genres    |
      | The First       | 1970-01-01  | pop, rock |
      | The Second      | 1970-01-02  | pop       |
    And Exists playlist registered by "user1"
      | name            | date        | genres    |
      | The Third       | 1970-01-03  | pop       |
      | The Fourth      | 1970-01-04  | pop       |
      | The Fifth       | 1970-01-05  | pop       |
    And I login as user "user" with password "password"

  Scenario: List my playlists
    When I list playlists
    Then I'm viewing a list containing my playlists
      | name            |
      | The First       |
      | The Second      |
    And The list contains 2 playlists (my)

  Scenario: List all playlists
    When I list playlists
    Then I'm viewing a list containing all playlists
      | name            |
      | The First       |
      | The Second      |
      | The Third       |
      | The Fourth      |
      | The Fifth       |
    And The list contains 5 playlists (all)