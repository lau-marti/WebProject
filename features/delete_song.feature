Feature: Delete Song
  In order to demonstrate that songs can be deleted, we will need a playlist, which contains a song
  Delete the song
  I check after deleting the song in total add one song less in the playlist

  Background: There is a registered user
    Given Create a user "user" with password "password"
    And Create playlist "The First" registered by "user"
      | name      | date       | genres    |
      | The First | 1970-01-01 | pop, rock |
    And Playlist "The First" registered by "user" contains the songs
      | song_title        | album | duration |
      | Shape of You | Manolo | 00:04:30 |

    Given Create a user "user1" with password "password"
    And Create playlist "Playlist1" registered by "user1"
      | name      | date       | genres    |
      | Playlist1 | 1970-01-01 | pop, rock |
    And Playlist "Playlist1" registered by "user" contains the songs
      | song_title        | album | duration |
      | Dragon Ball Rap | Joel Blanc | 00:04:30 |

  Scenario: Delete a song from the playlist
    Given User "user" login with password "password"
    And I go to the playlist detail page for "The First"
    And I remember the number of songs in the playlist
    When I delete a song with name "Shape of You" from the playlist
    Then the playlist should contain 1 fewer song

  Scenario: Try delete song from playlist of other user
    Given User "user" login with password "password"
    And I go to the playlist detail page for "Playlist1"
    And I remember the number of songs in the playlist
    When I try to delete song with name "Dragon Ball Rap" from the playlist makes exception


