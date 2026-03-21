# Behave BDD Guide (Python Framework)

This project uses Python Behave for BDD, not TypeScript Cucumber.js.

## Why This Changed

An older guide version was left from a previous TypeScript/Cucumber setup. The active framework in this repository is Python Playwright + Pytest + Behave.

## Quick Start

Run all BDD features:

```bash
python -m behave features
```

Run smoke BDD only:

```bash
python -m behave features --tags @smoke
```

Validate step mapping only (no browser execution):

```bash
python -m behave features --dry-run
```

Run a single feature file:

```bash
python -m behave features/user-authentication.feature
```

Run by feature line number:

```bash
python -m behave features/user-authentication.feature:20
```

Generate JUnit output for reporting:

```bash
python -m behave features --junit --junit-directory test-results/behave-junit
```

## BDD Project Structure

```text
features/
|-- environment.py
|-- user-registration.feature
|-- user-authentication.feature
|-- product-management.feature
`-- steps/
    |-- user_registration_steps.py
    |-- user_authentication_steps.py
    `-- product_management_steps.py

behave.ini
```

## Current Feature Coverage

User Registration (TC01):
- Register user
- Fill account and address details
- Verify account created and deleted

User Authentication (TC02-TC04):
- Login with valid credentials
- Login with invalid credentials (negative)
- Logout flow

Product Management (TC07-TC12):
- Navigate to test cases page
- View products and product detail
- Search products
- Add products to cart

## Tags in Use

- @smoke
- @user-registration
- @authentication
- @products
- @search
- @cart
- @negative

## Behave Configuration

Configuration is in behave.ini and uses the features path and progress formatter.

Example:

```ini
[behave]
paths = features
stdout_capture = false
stderr_capture = false
log_capture = false
format = progress2
```

## Example Feature and Step

Feature snippet:

```gherkin
Feature: User Registration
  @smoke @user-registration
  Scenario: TC01 - Register User with valid details
    Given I navigate to the home page
    When I verify that home page is visible successfully
    And I click on 'Signup / Login' button
```

Step definition snippet (Python):

```python
from behave import given


@given("I navigate to the home page")
def step_navigate_home(context):
    context.home_page.navigate_to()
```

## Reporting

Generate Behave JUnit output:

```bash
python -m behave features --junit --junit-directory test-results/behave-junit
```

Create summary from Behave JUnit files:

```bash
python scripts/summarize_junit.py \
  --input test-results/behave-junit \
  --output-json test-results/behave-summary.json \
  --output-md test-results/behave-summary.md \
  --title "Behave BDD Summary"
```

## CI Integration

BDD runs in GitHub Actions workflow .github/workflows/python-pytest.yml using job test-behave.

Tag behavior:
- Pull requests: @smoke
- Push/main runs: full BDD suite by default
- Manual dispatch with test_scope=smoke: @smoke

BDD artifact name pattern:
- behave-bdd-results-<run_number>

Artifacts include:
- test-results/behave-output.txt
- test-results/behave-junit/*
- test-results/behave-summary.json
- test-results/behave-summary.md

## Debugging Tips

Run only one tag group:

```bash
python -m behave features --tags @authentication
```

Stop early on first failure:

```bash
python -m behave features --stop
```

Use dry-run to find undefined steps quickly:

```bash
python -m behave features --dry-run
```

## Best Practices

1. Keep step definitions reusable and business-readable.
2. Keep selectors and UI actions in page objects, not in feature files.
3. Use tags to control fast PR smoke runs versus full regression.
4. Prefer stable test data and fallback flows for shared environments.
5. Keep feature files focused on behavior, not implementation details.

## References

- Behave docs: https://behave.readthedocs.io/
- Gherkin reference: https://cucumber.io/docs/gherkin/
