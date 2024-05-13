Feature: Logout
  In order to ensure the security of my account
  As a registered user
  I want to logout from the application

  Background: User is logged in
    Given Exists a user "user" with password "password"

  Scenario: Successful logout
    Given I login as user "user" with password "password"
    When I click on the "Logout" button
    Then I should be redirected to the "Login" page
