# Cucumber BDD Integration Guide

This guide covers the Cucumber BDD (Behavior Driven Development) framework integration with your Playwright automation project.

## 🚀 Quick Start

### Running Cucumber Tests

```bash
# Run all cucumber tests
npm run cucumber

# Run tests with specific tags
npm run cucumber:smoke          # Run smoke tests only
npm run cucumber:products       # Run product-related tests
npm run cucumber:authentication # Run authentication tests
npm run cucumber:user-registration # Run user registration tests

# Generate HTML report after test execution
npm run cucumber:report
```

## 📁 Project Structure

```
features/
├── support/
│   └── world.ts                    # World context with page objects
├── step-definitions/
│   ├── user-registration.steps.ts # User registration step definitions
│   ├── user-authentication.steps.ts # Authentication step definitions
│   └── product-management.steps.ts # Product management step definitions
├── user-registration.feature       # User registration scenarios
├── user-authentication.feature     # Authentication scenarios
└── product-management.feature      # Product management scenarios
```

## 🎯 Feature Coverage

### User Registration (TC01)
- Register new user with valid details
- Fill account and address information
- Verify account creation and deletion

### User Authentication (TC02-TC04)
- Login with correct credentials
- Login with incorrect credentials (negative test)
- Logout functionality

### Product Management (TC07-TC12)
- Verify test cases page
- View all products and product details
- Search products
- Add products to cart

## 🏷️ Tags Available

- `@smoke` - Critical smoke tests
- `@user-registration` - User registration tests
- `@authentication` - Authentication tests
- `@products` - Product management tests
- `@search` - Search functionality tests
- `@cart` - Shopping cart tests
- `@negative` - Negative test scenarios

## 📄 Feature Files

### Example Feature File Structure

```gherkin
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
    # ... more steps
```

## 🔧 Configuration

### Cucumber Configuration (`cucumber.js`)
```javascript
const common = [
  'features/**/*.feature',                // Feature files location
  '--require-module ts-node/register',    // TypeScript support
  '--require features/**/*.ts',           // Step definitions
  '--format progress-bar',                // Progress display
  '--format json:reports/cucumber-report.json', // JSON report
  '--format html:reports/cucumber-report.html', // HTML report
  '--format @cucumber/pretty-formatter',   // Console output
  '--publish-quiet'
].join(' ');
```

### World Context (`features/support/world.ts`)
The World context provides:
- Browser and page management
- Page object initialization
- Test setup and teardown
- Shared state between steps

## 📊 Reporting

### Available Reports
1. **JSON Report**: `reports/cucumber-report.json`
2. **HTML Report**: `reports/cucumber-report.html`
3. **Console Output**: Real-time progress and results

### Report Features
- Test execution summary
- Step-by-step results
- Screenshots on failure (if configured)
- Execution metadata (browser, platform, etc.)

## 🐛 Debugging

### Running Single Feature
```bash
npx cucumber-js features/user-registration.feature
```

### Running Single Scenario
```bash
npx cucumber-js features/user-registration.feature:10  # Line number 10
```

### Debug Mode
Add `@only` tag to scenario for focused execution:
```gherkin
@only @smoke
Scenario: Debug this scenario
```

## 🔄 Converting Existing Tests

To convert existing Playwright specs to Cucumber:

1. **Identify Test Steps**: Break down spec into Given/When/Then steps
2. **Create Feature File**: Write user story and scenarios
3. **Create Step Definitions**: Implement step functions
4. **Add Tags**: Categorize scenarios with appropriate tags

### Example Conversion

**Original Playwright Test:**
```typescript
test('Register User', async ({ homePage, loginPage }) => {
  await homePage.navigateTo();
  await homePage.clickSignupLogin();
  // ... more steps
});
```

**Cucumber Feature:**
```gherkin
Scenario: Register User
  Given I navigate to the home page
  When I click on 'Signup / Login' button
  # ... more steps
```

**Step Definition:**
```typescript
Given('I navigate to the home page', async function (this: CustomWorld) {
  await this.automationExerciseHomePage.navigateTo();
});
```

## 📝 Best Practices

1. **Use Descriptive Scenario Names**: Make them business-readable
2. **Keep Steps Reusable**: Write generic steps that can be reused
3. **Use Proper Tags**: Organize tests with meaningful tags
4. **Background Steps**: Use `Background:` for common setup steps
5. **Data Tables**: Use tables for complex test data
6. **Scenario Outlines**: Use for data-driven testing

### Example Data Table
```gherkin
When I fill in address information
  | firstName | lastName | company  | address1    | country |
  | Test      | User     | TestCorp | 123 Main St | India   |
```

### Example Scenario Outline
```gherkin
Scenario Outline: Login with different credentials
  When I login with email "<email>" and password "<password>"
  Then I should see "<result>"
  
  Examples:
    | email           | password    | result     |
    | valid@test.com  | password123 | success    |
    | invalid@test.com| wrongpass   | error      |
```

## 🚀 Next Steps

1. **Add More Features**: Convert remaining test cases (TC13-TC26)
2. **Enhance Reporting**: Add screenshots and videos to reports
3. **CI/CD Integration**: Configure pipeline execution
4. **Cross-Browser Support**: Extend for multiple browsers
5. **API Testing**: Add API step definitions for hybrid testing

## 📚 Resources

- [Cucumber.js Documentation](https://cucumber.io/docs/cucumber/)
- [Playwright Documentation](https://playwright.dev/)
- [BDD Best Practices](https://cucumber.io/docs/bdd/)
- [Gherkin Syntax Reference](https://cucumber.io/docs/gherkin/)
