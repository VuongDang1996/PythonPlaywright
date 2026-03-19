Feature: User Authentication
  As a registered user
  I want to login and logout
  So that I can access my account

  @smoke @authentication
  Scenario: TC02 - Login User with correct email and password
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Signup / Login' button
    Then I should see 'Login to your account' is visible
    When I enter correct email "test@example.com" and password "password123"
    And I click 'Login' button
    Then I should see 'Logged in as username' is visible
    When I click 'Delete Account' button
    Then I should see 'ACCOUNT DELETED!' is visible

  @smoke @authentication @negative
  Scenario: TC03 - Login User with incorrect email and password
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Signup / Login' button
    Then I should see 'Login to your account' is visible
    When I enter incorrect email "invalid@example.com" and password "wrongpassword"
    And I click 'Login' button
    Then I should see error message 'Your email or password is incorrect!'

  @smoke @authentication
  Scenario: TC04 - Logout User
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Signup / Login' button
    And I login with valid credentials
    Then I should see 'Logged in as username' is visible
    When I click 'Logout' button
    Then I should be navigated to login page
    And I should see 'Login to your account' is visible
