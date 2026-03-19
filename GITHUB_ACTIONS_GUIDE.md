# 🚀 GitHub Actions Configuration for Individual Tests

This guide explains how to use the GitHub Actions workflow specifically configured for running individual test cases in the `tests/specs/automation-exercise/individual-tests` folder.

## 📋 Workflow Overview

The **Individual Tests with Allure Report** workflow is designed to:
- Run only tests from the `individual-tests` folder
- Generate comprehensive Allure reports
- Support multiple browsers and test patterns
- Deploy reports to GitHub Pages (on main branch)
- Provide detailed test summaries

## 🎯 Workflow Triggers

### 1. Automatic Triggers
- **Push to main/develop**: When changes are made to:
  - `tests/specs/automation-exercise/individual-tests/**`
  - Related framework files (pages, fixtures, data, utils)
  - Workflow configuration file
- **Pull Requests**: Same path-based triggers as push events

### 2. Manual Trigger (workflow_dispatch)
You can manually trigger the workflow with custom parameters:

#### Available Options:
- **Browser**: Choose from:
  - `chromium` (default)
  - `firefox`
  - `webkit`
  - `all` (runs on all browsers)

- **Test Pattern**: Filter tests by:
  - `all` (default - runs all individual tests)
  - `smoke` (runs only @smoke tagged tests)
  - `regression` (runs only @regression tagged tests)
  - `tc01` (runs specific test case)
  - `tc01-tc05` (runs range of test cases)

- **Parallel Workers**: Number of parallel workers (default: 4)

## 🔧 How to Use

### Manual Execution
1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Individual Tests with Allure Report** workflow
4. Click **Run workflow** button
5. Choose your options:
   ```
   Browser: chromium
   Test Pattern: all
   Parallel Workers: 4
   ```
6. Click **Run workflow**

### Automatic Execution
The workflow runs automatically when you:
- Push code changes to main/develop branches
- Create pull requests affecting the individual tests

## 📊 What the Workflow Does

### 1. Test Execution
- Installs dependencies and Playwright browsers
- Runs tests from `tests/specs/automation-exercise/individual-tests` folder
- Supports multiple browsers simultaneously
- Uses parallel execution for faster results

### 2. Report Generation
- **Playwright HTML Report**: Standard Playwright test results
- **Allure Report**: Enhanced reporting with:
  - Step-by-step execution details
  - Screenshots on failures
  - Test metadata (Epic, Feature, Story)
  - Historical trends
  - Test categorization

### 3. Artifact Upload
- Test results and screenshots
- Both HTML and Allure reports
- Retained for 30 days

### 4. GitHub Pages Deployment
- On main branch: Deploys Allure report to GitHub Pages
- Accessible at: `https://[username].github.io/[repo]/individual-tests-report-[run-number]`

## 📁 Test Coverage

The workflow executes **26 individual test cases**:

| Test Range | Description | Count |
|------------|-------------|-------|
| TC01-TC05 | Authentication tests | 5 |
| TC06-TC08 | Product catalog tests | 3 |
| TC09-TC13 | Shopping cart tests | 5 |
| TC14-TC16 | Checkout/Order tests | 3 |
| TC17-TC26 | Advanced functionality | 10 |

## 🎯 Example Usage Scenarios

### Run All Tests on Chrome
```yaml
Browser: chromium
Test Pattern: all
Parallel Workers: 4
```

### Run Only Smoke Tests on All Browsers
```yaml
Browser: all
Test Pattern: smoke
Parallel Workers: 2
```

### Run Specific Test Range on Firefox
```yaml
Browser: firefox
Test Pattern: tc01-tc05
Parallel Workers: 2
```

### Run Regression Tests with High Parallelism
```yaml
Browser: chromium
Test Pattern: regression
Parallel Workers: 8
```

## 📈 Reports and Artifacts

After workflow completion, you'll find:

### 1. GitHub Summary
- Test execution status
- Browser-specific results
- Links to reports
- Execution details

### 2. Artifacts (Downloads)
- `test-results-[browser]-[run-number]`: Raw test data
- `playwright-report-[browser]-[run-number]`: Standard Playwright report
- `allure-report-combined-[run-number]`: Combined Allure report

### 3. GitHub Pages (Main Branch Only)
- Live Allure report accessible via web browser
- Includes all test results, trends, and detailed analysis

## 🔍 Troubleshooting

### Common Issues:

1. **Tests Failing**: Check individual test logs in artifacts
2. **Report Not Generated**: Verify Allure results in artifacts
3. **GitHub Pages Not Deploying**: Ensure you're on main branch and have GitHub Pages enabled

### Debug Steps:
1. Download and examine test artifacts
2. Check workflow logs for detailed error messages
3. Verify test file paths and patterns
4. Ensure all dependencies are properly configured

## 🛠️ Local Development

To run the same tests locally:

```bash
# Run all individual tests
npm run test:individual

# Run specific pattern
npx playwright test tests/specs/automation-exercise/individual-tests --grep="@smoke"

# Generate Allure report
npm run test:allure
npm run report:allure-generate
```

## 📝 Configuration Files

Key files for the workflow:
- `.github/workflows/individual-tests.yml`: Main workflow configuration
- `package.json`: npm scripts for test execution
- `playwright.config.ts`: Playwright configuration
- `tests/utils/allure-helpers.ts`: Allure reporting utilities

This workflow ensures consistent, comprehensive testing of your individual test cases with professional reporting and easy access to results.
