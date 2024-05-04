Feature: Create A Playlist
  To create a playlist
  As a user
  I want to register the playlist, along with its name

  Background: There is a registered user
    Given Exists a user "user" with password "password"

  Scenario: Register playlist name
    Given I login as user "user" with password "password"
    When I register playlist
      | name        |
      | Rock List   |
    Then I'm viewing the details page for playlist by "user"
      | name        |
      | Rock List   |
    And There are 1 restaurants

  Scenario: Register just restaurant name and city
    Given I login as user "user" with password "password"
    When I register restaurant
      | name        | city      | country   |
      | The Tavern  | London    | England   |
    Then I'm viewing the details page for restaurant by "user"
      | name        | city      | country   |
      | The Tavern  | London    | England   |
    And There are 1 restaurants

  Scenario: Try to register restaurant but not logged in
    Given I'm not logged in
    When I register restaurant
      | name        |
      | The Tavern  |
    Then I'm redirected to the login form
    And There are 0 restaurants