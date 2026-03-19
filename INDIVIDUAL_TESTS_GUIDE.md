# Running Individual Test Cases - Quick Reference

## Overview
This document provides various commands to run individual test cases from the `tests/specs/automation-exercise/individual-tests/` folder.

## Prerequisites
1. Ensure all dependencies are installed: `npm install`
2. Make sure the Playwright browsers are installed: `npx playwright install`

## Basic Commands

### 1. Run a Single Test Case
```bash
# Run specific test file
npx playwright test tests/specs/automation-exercise/individual-tests/tc01-register-user.spec.ts

# Run with specific browser
npx playwright test tests/specs/automation-exercise/individual-tests/tc02-login-user-correct.spec.ts --project=chromium

# Run in headed mode (shows browser window)
npx playwright test tests/specs/automation-exercise/individual-tests/tc03-login-user-incorrect.spec.ts --project=chromium --headed
```

### 2. Run Multiple Test Cases
```bash
# Run all tests in the individual-tests folder
npx playwright test tests/specs/automation-exercise/individual-tests/

# Run tests by pattern
npx playwright test tests/specs/automation-exercise/individual-tests/tc0[1-5]*.spec.ts

# Run tests by tag
npx playwright test --grep "@smoke"
npx playwright test --grep "@regression"
```

### 3. Debug Mode
```bash
# Run in debug mode (step through test)
npx playwright test tests/specs/automation-exercise/individual-tests/tc02-login-user-correct.spec.ts --debug

# Run specific test with debug
npx playwright test --debug --grep "TC04 - Logout User"
```

### 4. Run with Different Browsers
```bash
# Chrome/Chromium
npx playwright test tests/specs/automation-exercise/individual-tests/tc07-verify-test-cases-page.spec.ts --project=chromium

# Firefox
npx playwright test tests/specs/automation-exercise/individual-tests/tc08-verify-products-and-detail.spec.ts --project=firefox

# Safari/WebKit
npx playwright test tests/specs/automation-exercise/individual-tests/tc09-search-product.spec.ts --project=webkit

# Mobile Chrome
npx playwright test tests/specs/automation-exercise/individual-tests/tc10-verify-subscription-home.spec.ts --project=mobile-chrome
```

## Test Cases Available

| Test Case | File Name | Description | Tags |
|-----------|-----------|-------------|------|
| TC01 | tc01-register-user.spec.ts | Register new user | @smoke |
| TC02 | tc02-login-user-correct.spec.ts | Login with correct credentials | @smoke |
| TC03 | tc03-login-user-incorrect.spec.ts | Login with incorrect credentials | @regression |
| TC04 | tc04-logout-user.spec.ts | Logout functionality | @smoke |
| TC05 | tc05-register-existing-email.spec.ts | Register with existing email | @regression |
| TC06 | tc06-contact-us-form.spec.ts | Contact form submission | @regression |
| TC07 | tc07-verify-test-cases-page.spec.ts | Navigate to test cases page | @smoke |
| TC08 | tc08-verify-products-and-detail.spec.ts | View products and details | @smoke |
| TC09 | tc09-search-product.spec.ts | Search for products | @regression |
| TC10 | tc10-verify-subscription-home.spec.ts | Newsletter subscription on home | @regression |
| TC11 | tc11-verify-subscription-cart.spec.ts | Newsletter subscription on cart | @regression |
| TC12 | tc12-add-products-cart.spec.ts | Add multiple products to cart | @regression |
| TC13 | tc13-verify-product-quantity-cart.spec.ts | Verify product quantity in cart | @regression |
| TC14 | tc14-place-order-register-while-checkout.spec.ts | Place order with registration | @regression |
| TC15 | tc15-place-order-register-before-checkout.spec.ts | Place order after registration | @regression |
| TC16 | tc16-place-order-login-before-checkout.spec.ts | Place order with existing user | @regression |
| TC17 | tc17-remove-products-cart.spec.ts | Remove products from cart | @regression |
| TC18 | tc18-view-category-products.spec.ts | View products by category | @regression |
| TC19 | tc19-view-cart-brand-products.spec.ts | View products by brand | @regression |
| TC20 | tc20-search-products-verify-cart-after-login.spec.ts | Search and cart persistence | @regression |
| TC21 | tc21-add-review-product.spec.ts | Add product review | @regression |
| TC22 | tc22-add-cart-recommended-items.spec.ts | Add recommended items to cart | @regression |
| TC23 | tc23-verify-address-details-checkout.spec.ts | Verify address in checkout | @regression |
| TC24 | tc24-download-invoice-after-purchase.spec.ts | Download invoice after order | @regression |
| TC25 | tc25-verify-scroll-up-arrow-button.spec.ts | Scroll up with arrow button | @regression |
| TC26 | tc26-verify-scroll-up-without-arrow-button.spec.ts | Scroll up without arrow | @regression |

## Useful Options

### Reporting
```bash
# Generate HTML report
npx playwright test tests/specs/automation-exercise/individual-tests/tc02-login-user-correct.spec.ts --reporter=html

# Show report after test
npx playwright show-report
```

### Parallel Execution
```bash
# Run tests in parallel (default)
npx playwright test tests/specs/automation-exercise/individual-tests/ --workers=4

# Run tests sequentially
npx playwright test tests/specs/automation-exercise/individual-tests/ --workers=1
```

### Timeout Control
```bash
# Increase timeout for slow tests
npx playwright test tests/specs/automation-exercise/individual-tests/tc01-register-user.spec.ts --timeout=60000
```

### Retry Failed Tests
```bash
# Retry failed tests
npx playwright test tests/specs/automation-exercise/individual-tests/ --retries=2
```

## Examples

### Quick Smoke Test Run
```bash
npx playwright test --grep "@smoke" --project=chromium --headed
```

### Full Regression Suite
```bash
npx playwright test tests/specs/automation-exercise/individual-tests/ --project=chromium
```

### Debug Specific Failing Test
```bash
npx playwright test tests/specs/automation-exercise/individual-tests/tc01-register-user.spec.ts --debug --project=chromium
```

### Run Test and Keep Browser Open
```bash
npx playwright test tests/specs/automation-exercise/individual-tests/tc02-login-user-correct.spec.ts --headed --project=chromium
```

## Troubleshooting

1. **Timeout Issues**: Add `--timeout=60000` for longer timeout
2. **Network Issues**: Use `--project=chromium` to run only one browser
3. **Element Not Found**: Use `--debug` to step through and inspect elements
4. **Multiple Element Errors**: Check selectors in page objects for `.first()` usage

## Best Practices

1. **Start with one browser**: Use `--project=chromium` for initial testing
2. **Use headed mode**: Add `--headed` to see what's happening
3. **Debug step by step**: Use `--debug` for failing tests
4. **Check reports**: Always run `npx playwright show-report` after tests
5. **Run in isolation**: Test individual files first before running suites
