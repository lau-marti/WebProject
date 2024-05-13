Feature: Delete Song
  In order to demonstrate that songs can be deleted, we will need a playlist, which contains a song
  Delete the song
  I check after deleting the song in total add one song less in the playlist

  Background: There is a registered user and playlist
    Given Exists a user "user" with password "password"
    And Exists a user "user1" with password "password"
    And Exists playlist registered by "user"
      | name            | description         | date          | genres      |
      | Famous          | Form singer Famous  | 2023-05-23    | pop, rock   |
      | Unknown         |                     | 2003-08-25    | pop         |
    And Exists song at playlist "Famous" by "user"
      | name      |
      | Hello     |
    And Exists song at playlist "Famous" by "user"
      | name      |
      | Pepito    |


  Scenario: Delete a song to a playlist
    Given I login as user "user" with password "password"
    When I view the details for playlist "Famous"
    And I delete the song "Hello" form playlist "Famous"
    Then I'm viewing a playlist songs list containing
      | name     |
      | Pepito    |
    And The list contains 1 songs

  Scenario: Try to delete a song to a playlist if not are login
    When I view the details for playlist "Famous"
    Then There is no "Delete" link available
    When I delete the song "Hello" form playlist "Famous" directly
    Then I'm redirected to the login form

    
  Scenario: Try to delete a song to a playlist if user is not the owner
    Given I login as user "user1" with password "password"
    When I view the details for playlist "Famous"
    Then There is no "Delete" link available
    When I delete the song "Hello" form playlist "Famous" directly
    Then Server responds with page containing "403 Forbidden"




