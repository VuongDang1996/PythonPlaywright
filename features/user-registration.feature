Feature: User Registration
  As a potential user
  I want to register for an account
  So that I can access the website's features

  @smoke @user-registration
  Scenario: TC01 - Register User with valid details
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Signup / Login' button
    Then I should see 'New User Signup!' is visible
    When I enter name "TestUser" and email address
    And I click 'Signup' button
    Then I should see 'ENTER ACCOUNT INFORMATION' is visible
    When I fill in the account information with title "Mr", password "password123"
    And I select date of birth "15", "January", "1990"
    And I check newsletter and offers checkboxes
    And I fill in address information
      | firstName | lastName | company  | address1    | country | state | city    | zipcode | mobileNumber |
      | Test      | User     | TestCorp | 123 Main St | India   | Delhi | New Delhi | 110001  | 9876543210   |
    And I click 'Create Account' button
    Then I should see 'ACCOUNT CREATED!' is visible
    When I click 'Continue' button
    Then I should see 'Logged in as username' is visible
    When I click 'Delete Account' button
    Then I should see 'ACCOUNT DELETED!' is visible
    And I click 'Continue' button
