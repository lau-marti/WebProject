Feature: Register Song
  In order to keep track of the dishes I eat
  As a user
  I want to register a dish in the corresponding restaurant together with its details

  Background: There is a registered user and restaurant
    Given Exists a user "user" with password "password"
    And Exists playlist registered by "user"
      | name            |
      | The Tavern      |

  Scenario: Register just song name
    Given I login as user "user" with password "password"
    When I register song at playlist "The Tavern"
      | name            |
      | Fish and Chips  |
    Then I'm viewing the details page for song at playlist "The Tavern" by "user"
      | name            |
      | Fish and Chips  |
    And There are 1 songs

