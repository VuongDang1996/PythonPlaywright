Feature: Product Management
  As a user
  I want to browse and search products
  So that I can find items to purchase

  @smoke @products
  Scenario: TC07 - Verify Test Cases Page
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Test Cases' button
    Then I should be navigated to test cases page successfully

  @smoke @products
  Scenario: TC08 - Verify All Products and product detail page
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Products' button
    Then I should be navigated to ALL PRODUCTS page successfully
    And I should see the products list is visible
    When I click on 'View Product' of first product
    Then I should be landed on product detail page
    And I should see product name, category, price, availability, condition, brand

  @smoke @products @search
  Scenario: TC09 - Search Product
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Products' button
    Then I should be navigated to ALL PRODUCTS page successfully
    When I enter product name "Blue Top" in search input
    And I click search button
    Then I should see 'SEARCHED PRODUCTS' is visible
    And I should see all the products related to search are visible

  @smoke @products @cart
  Scenario: TC12 - Add Products in Cart
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Products' button
    Then I should be navigated to ALL PRODUCTS page successfully
    When I hover over first product and click 'Add to cart'
    And I click 'Continue Shopping' button
    And I hover over second product and click 'Add to cart'
    And I click 'View Cart' button
    Then I should see both products are added to Cart
    And I should see their prices, quantity and total price
