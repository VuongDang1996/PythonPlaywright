# Automation Exercise Test Implementation Guide

This guide explains how to implement and run the 26 test cases for the Automation Exercise website using our Playwright TypeScript framework with Page Object Model (POM) design pattern.

## 📋 Test Cases Overview

We have implemented all 26 test cases covering:
- User Registration and Authentication (TC01-TC05)
- Contact Form and Navigation (TC06-TC07)
- Product Browsing and Search (TC08-TC09, TC21)
- Subscription Features (TC10-TC11)
- Shopping Cart Operations (TC12-TC13, TC17, TC22)
- Order Management (TC14-TC16, TC23-TC24)
- Category and Brand Navigation (TC18-TC19)
- Search and Cart Persistence (TC20)
- Scroll Functionality (TC25-TC26)

## 🏗️ Project Structure

```
tests/
├── pages/                                    # Page Object classes
│   ├── AutomationExerciseHomePage.ts        # Main home page
│   ├── AutomationExerciseContactUsPage.ts   # Contact form page
│   ├── AutomationExerciseProductsPage.ts    # Products listing page
│   ├── AutomationExerciseProductDetailPage.ts # Product detail page
│   ├── AutomationExerciseCartPage.ts        # Shopping cart page
│   └── auth/
│       ├── AutomationExerciseLoginPage.ts   # Login/Signup page
│       └── AutomationExerciseSignupPage.ts  # Account creation page
├── fixtures/
│   └── automation-exercise-fixtures.ts      # Page object fixtures
├── data/
│   └── automation-exercise-data.ts          # Test data and interfaces
└── specs/
    └── automation-exercise/
        └── automation-exercise.spec.ts      # All 26 test cases
```

## 🚀 Getting Started

### 1. Environment Setup

Update your `.env` file with the correct base URL:

```env
BASE_URL=http://automationexercise.com
TEST_USERNAME=your-test-email@example.com
TEST_PASSWORD=your-test-password
```

### 2. Running All Test Cases

```bash
# Run all Automation Exercise tests
npm test -- tests/specs/automation-exercise/

# Run specific test by name
npm test -- --grep "TC01 - Register User"

# Run tests with specific tags
npm test -- --grep "@smoke"
npm test -- --grep "@regression"

# Run tests in headed mode for debugging
npm run test:headed -- tests/specs/automation-exercise/
```

### 3. Running Individual Test Categories

```bash
# Authentication tests (TC01-TC05)
npm test -- --grep "TC0[1-5]"

# Product-related tests (TC08-TC09, TC12-TC13, TC21-TC22)
npm test -- --grep "TC(08|09|12|13|21|22)"

# Subscription tests (TC10-TC11)
npm test -- --grep "TC1[01]"

# Scroll functionality tests (TC25-TC26)
npm test -- --grep "TC2[56]"
```

## 📝 Implemented Test Cases

### ✅ Completed Test Cases

| Test Case | Status | Description | Tags |
|-----------|---------|-------------|------|
| TC01 | ✅ | Register User | @smoke |
| TC02 | ✅ | Login User with Correct Credentials | @smoke |
| TC03 | ✅ | Login User with Incorrect Credentials | @regression |
| TC04 | ✅ | Logout User | @smoke |
| TC05 | ✅ | Register User with Existing Email | @regression |
| TC06 | ✅ | Contact Us Form | @regression |
| TC07 | ✅ | Verify Test Cases Page | @smoke |
| TC08 | ✅ | Verify All Products and Product Detail Page | @smoke |
| TC09 | ✅ | Search Product | @regression |
| TC10 | ✅ | Verify Subscription in Home Page | @regression |
| TC11 | ✅ | Verify Subscription in Cart Page | @regression |
| TC12 | ✅ | Add Products in Cart | @regression |
| TC13 | ✅ | Verify Product Quantity in Cart | @regression |
| TC21 | ✅ | Add Review on Product | @regression |
| TC22 | ✅ | Add to Cart from Recommended Items | @regression |
| TC25 | ✅ | Verify Scroll Up Using Arrow Button | @regression |
| TC26 | ✅ | Verify Scroll Up Without Arrow Button | @regression |

### 🚧 Test Cases to Implement

The following test cases require additional page objects and can be implemented using the same pattern:

| Test Case | Description | Required Pages |
|-----------|-------------|----------------|
| TC14 | Place Order: Register While Checkout | CheckoutPage, PaymentPage |
| TC15 | Place Order: Register Before Checkout | CheckoutPage, PaymentPage |
| TC16 | Place Order: Login Before Checkout | CheckoutPage, PaymentPage |
| TC17 | Remove Products From Cart | CartPage (extend existing) |
| TC18 | View Category Products | CategoryPage |
| TC19 | View & Cart Brand Products | BrandPage |
| TC20 | Search Products and Verify Cart After Login | (combine existing pages) |
| TC23 | Verify Address Details in Checkout Page | CheckoutPage |
| TC24 | Download Invoice After Purchase Order | CheckoutPage, PaymentPage |

## 🔧 Adding New Test Cases

### Step 1: Create Required Page Objects

For checkout functionality, create new page objects:

```typescript
// tests/pages/AutomationExerciseCheckoutPage.ts
export class AutomationExerciseCheckoutPage extends BasePage {
  readonly deliveryAddress: Locator;
  readonly billingAddress: Locator;
  readonly orderReview: Locator;
  readonly commentTextarea: Locator;
  readonly placeOrderButton: Locator;
  
  // Implementation methods...
}
```

### Step 2: Add Page Object to Fixtures

```typescript
// tests/fixtures/automation-exercise-fixtures.ts
type AutomationExercisePageFixtures = {
  // ... existing fixtures
  checkoutPage: AutomationExerciseCheckoutPage;
  paymentPage: AutomationExercisePaymentPage;
};

export const test = base.extend<AutomationExercisePageFixtures>({
  // ... existing fixtures
  checkoutPage: async ({ page }, use) => {
    const checkoutPage = new AutomationExerciseCheckoutPage(page);
    await use(checkoutPage);
  },
});
```

### Step 3: Implement Test Case

```typescript
test('TC14 - Place Order: Register While Checkout @regression', async ({ 
  homePage, 
  productsPage, 
  cartPage, 
  loginPage, 
  signupPage, 
  checkoutPage, 
  paymentPage 
}) => {
  // Test implementation following the same pattern
});
```

## 🎯 Page Object Design Patterns

### 1. Element Locators

Use robust locators that are less likely to break:

```typescript
// ✅ Good - Use data attributes
readonly signupButton = page.locator('button[data-qa="signup-button"]');

// ✅ Good - Use text content
readonly newUserSignupTitle = page.locator('h2:has-text("New User Signup!")');

// ✅ Good - Use role-based selectors
readonly submitButton = page.getByRole('button', { name: 'Submit' });

// ❌ Avoid - CSS classes and complex selectors
readonly submitButton = page.locator('.btn.btn-primary.submit-btn');
```

### 2. Method Naming

Follow consistent naming conventions:

```typescript
// Action methods - verb + noun
async clickSignupButton(): Promise<void>
async fillContactForm(data: ContactFormData): Promise<void>
async selectCountry(country: string): Promise<void>

// Query methods - is/are/get + descriptor
async isErrorVisible(): Promise<boolean>
async areProductsDisplayed(): Promise<boolean>
async getErrorMessage(): Promise<string>

// Wait methods - waitFor + descriptor
async waitForPageReady(): Promise<void>
async waitForProductsToLoad(): Promise<void>
```

### 3. Data Handling

Use interfaces for type safety:

```typescript
// Define interfaces for complex data
interface UserRegistrationData {
  name: string;
  email: string;
  password: string;
  // ... other fields
}

// Use in page methods
async registerUser(userData: UserRegistrationData): Promise<void> {
  await this.nameInput.fill(userData.name);
  await this.emailInput.fill(userData.email);
  // ... rest of implementation
}
```

## 🧪 Test Data Management

### Using Test Data

```typescript
import { SAMPLE_REGISTRATION_DATA, TEST_USERS } from '@data/automation-exercise-data';

test('Register new user', async ({ homePage, loginPage, signupPage }) => {
  // Use predefined test data
  const userData = {
    ...SAMPLE_REGISTRATION_DATA,
    email: `test${Date.now()}@example.com`, // Generate unique email
  };
  
  await homePage.navigateTo();
  await homePage.clickSignupLogin();
  await loginPage.signupUser(userData.name, userData.email);
  // ... continue with test
});
```

### Dynamic Test Data

```typescript
// Generate unique data for each test run
const generateUserData = () => ({
  name: `TestUser${Date.now()}`,
  email: `test${Date.now()}@example.com`,
  password: 'password123',
});
```

## 🔍 Debugging Tests
Run test case individuals : 
npx playwright test --debug --grep "TC01 - Register User"
npx playwright test --debug --grep "TC02 - Login User with Correct Email and Password"
npx playwright test --debug --grep "TC03 - Login User with Incorrect Email and Password"
npx playwright test --debug --grep "TC04 - Logout User"
npx playwright test --debug --grep "TC05 - Register User with Existing Email"
npx playwright test --debug --grep "TC06 - Contact Us Form"
npx playwright test --debug --grep "TC07 - Verify Test Cases Page"
npx playwright test --debug --grep "TC08 - Verify All Products and Product Detail Page"
npx playwright test --debug --grep "TC09 - Search Product"
npx playwright test --debug --grep "TC10 - Verify Subscription in Home Page"
npx playwright test --debug --grep "TC11 - Verify Subscription in Cart Page"
npx playwright test --debug --grep "TC12 - Add Products in Cart"
npx playwright test --debug --grep "TC13 - Verify Product Quantity in Cart"
npx playwright test --debug --grep "TC14 - Place Order: Register While Checkout"
npx playwright test --debug --grep "TC15 - Place Order: Register Before Checkout"
npx playwright test --debug --grep "TC16 - Place Order: Login Before Checkout"
npx playwright test --debug --grep "TC17 - Remove Products From Cart"
npx playwright test --debug --grep "TC18 - View Category Products"
npx playwright test --debug --grep "TC19 - View & Cart Brand Products"
npx playwright test --debug --grep "TC20 - Search Products and Verify Cart After Login"
npx playwright test --debug --grep "TC21 - Add Review on Product"
npx playwright test --debug --grep "TC22 - Add to Cart from Recommended Items"
npx playwright test --debug --grep "TC23 - Verify Address Details in Checkout Page"
npx playwright test --debug --grep "TC24 - Download Invoice After Purchase Order"
npx playwright test --debug --grep "TC25 - Verify Scroll Up Using Arrow Button"
npx playwright test --debug --grep "TC26 - Verify Scroll Up Without Arrow Button"

### 1. Visual Debugging

```bash
# Run in headed mode to see browser
npm run test:headed -- tests/specs/automation-exercise/

# Run with debug mode for step-by-step execution
npm run test:debug -- --grep "TC01"
```

### 2. Screenshots and Videos

```typescript
// Add custom screenshots in tests
test('TC01 - Register User', async ({ page, homePage }) => {
  await homePage.navigateTo();
  
  // Take screenshot at specific point
  await page.screenshot({ path: 'debug-home-page.png' });
  
  // Continue with test...
});
```

### 3. Console Logging

```typescript
// Add logging to page objects
async fillContactForm(data: ContactFormData): Promise<void> {
  console.log('Filling contact form with:', data);
  await this.nameInput.fill(data.name);
  await this.emailInput.fill(data.email);
  // ... rest of implementation
}
```

## 📊 Reporting

### Generate Test Reports

```bash
# Run tests and generate HTML report
npm test

# View the generated report
npm run report
```

### CI/CD Integration

The framework includes GitHub Actions workflows that will:
- Run all tests across multiple browsers
- Generate test reports
- Upload screenshots and videos on failures
- Comment on PRs with test results

## Python Behave BDD Execution Report

The repository also includes a Python Behave BDD layer under `features/`.

Run locally:

```bash
python -m behave features
python -m behave features --tags @smoke
python -m behave features --dry-run
python -m behave features --junit --junit-directory test-results/behave-junit
```

CI behavior:

- Workflow: `.github/workflows/python-pytest.yml`
- Job: `test-behave`
- Tag strategy:
  - Pull requests run `@smoke`
  - Push and default manual runs execute full BDD suite
  - Manual dispatch with `test_scope=smoke` runs `@smoke`
- Artifacts:
  - `behave-bdd-results-<run_number>`
  - includes `behave-output.txt`, JUnit XML files, `behave-summary.json`, and `behave-summary.md`

Recommended triage order for BDD failures:

1. Open workflow job logs for `test-behave`.
2. Read `behave-output.txt` to locate the first failing scenario and step.
3. Inspect `behave-summary.md` for pass/fail counts and durations.
4. Re-run only impacted scenarios locally with `--tags` or target feature path.

## 🔧 Customization

### Adding New Locators

When the website changes, update locators in page objects:

```typescript
// Update locator strategy if needed
readonly signupButton = page.locator('button[data-qa="signup-button"]');
// If data-qa is removed, fallback to text content
readonly signupButton = page.locator('button:has-text("Signup")');
```

### Environment-Specific Configuration

```typescript
// playwright.config.ts
const config = {
  use: {
    baseURL: process.env.BASE_URL || 'http://automationexercise.com',
    // Add environment-specific settings
  },
  projects: [
    {
      name: 'staging',
      use: { baseURL: 'https://staging.automationexercise.com' },
    },
    {
      name: 'production',
      use: { baseURL: 'https://automationexercise.com' },
    },
  ],
};
```

## 🚀 Best Practices

1. **Stable Locators**: Use data attributes and text content over CSS classes
2. **Page Readiness**: Always wait for pages to be ready before interactions
3. **Error Handling**: Implement proper error handling in page methods
4. **Test Isolation**: Each test should be independent and clean up after itself
5. **Data Management**: Use interfaces and constants for test data
6. **Parallel Execution**: Design tests to run independently in parallel
7. **Meaningful Assertions**: Use descriptive assertion messages
8. **Regular Maintenance**: Update locators when the application changes

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify that locators match the current website structure
3. Run tests in headed mode to see what's happening
4. Check the generated screenshots and videos
5. Update page objects if the website has changed

Happy Testing! 🎭
