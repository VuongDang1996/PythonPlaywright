# Python Playwright Framework Run Guide

This guide explains how to run the Python Playwright framework locally and in CI.

## 1. Prerequisites

- Python 3.12+
- pip
- Playwright browsers
- Java 17+ (only if you want to generate/view Allure HTML reports locally)

## 2. Install Dependencies

From the repository root:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m playwright install --with-deps chromium
```

If you run on Windows and `--with-deps` is not supported in your shell, use:

```powershell
python -m playwright install chromium
```

## 3. Configure Environment

Copy `.env.example` to `.env` and set values for your environment.

Minimum recommended values:

```env
BASE_URL=https://automationexercise.com
HEADLESS=true
DEFAULT_TIMEOUT_MS=30000
NAVIGATION_TIMEOUT_MS=60000
AE_VALID_USER_EMAIL=your-valid-user@example.com
AE_VALID_USER_PASSWORD=your-valid-password
```

## 4. Run Quality Gates (Recommended Before Tests)

```bash
python -m ruff check pytests/config pytests/components pytests/pages pytests/data pytests/conftest.py
python -m black --check pytests/config pytests/components pytests/pages pytests/data pytests/conftest.py
python -m mypy pytests/config pytests/components pytests/pages pytests/data pytests/conftest.py
```

## 5. Run Tests Locally

Run all tests:

```bash
python -m pytest pytests/specs --browser=chromium -q
```

Run smoke tests only:

```bash
python -m pytest pytests/specs --browser=chromium -m smoke -q
```

Run a single test file:

```bash
python -m pytest pytests/specs/automation_exercise/individual_tests/test_tc01_register_user.py --browser=chromium -q
```

Run in parallel (auto workers):

```bash
python -m pytest pytests/specs --browser=chromium -n auto --dist=loadscope -q
```

## 6. Run and Generate Reports Locally

Generate Allure raw results during test run:

```bash
python -m pytest pytests/specs --browser=chromium --alluredir=allure-results -q
```

Generate Allure HTML report:

```bash
allure generate allure-results --clean -o allure-report
```

Open the report:

```bash
allure open allure-report
```

Generate JUnit XML:

```bash
python -m pytest pytests/specs --browser=chromium --junitxml=test-results/junit-python.xml -q
```

Generate CI-style summary from JUnit:

```bash
python scripts/summarize_junit.py --input test-results/junit-python.xml --output-json test-results/summary.json --output-md test-results/summary.md --title "Local Python Summary"
```

Generate flaky trend update from summary:

```bash
python scripts/update_flaky_trend.py --summary-json test-results/summary.json --trend-file test-results/flaky-trend.json --output-json test-results/flaky-trend.json --output-md test-results/flaky-trend.md --run-id local --run-number 1 --workflow local --ref local --sha local --browser chromium --event manual
```

## 7. Run in GitHub Actions

Available workflows:

- `.github/workflows/python-pytest.yml`
  - Fast PR/main pipeline with quality gates, parallel workers, summary, flaky trend, and Allure publish flow.
- `.github/workflows/python-pytest-nightly.yml`
  - Nightly matrix pipeline (chromium/firefox/webkit) with retries, summaries, and combined Allure publishing.

Manual run options include browser, parallel workers, and test scope.

## 8. Troubleshooting

- Browser not found:
  - Re-run `python -m playwright install chromium`.
- Very slow or flaky run:
  - Use `-m smoke` first, then run the full suite.
  - Try a fixed worker count, for example `-n 4`, instead of `-n auto`.
- Missing report output:
  - Ensure `allure-results` exists and includes `.json` result files.
- Auth test failures:
  - Verify account environment variables in `.env`.

## 9. Useful Commands

Collect tests only:

```bash
python -m pytest --collect-only pytests/specs -q
```

Run with headed browser for debugging:

```bash
python -m pytest pytests/specs --browser=chromium --headed -q
```

Run with trace/screenshot artifacts enabled from environment:

```bash
TRACE_ON_FAILURE=true SCREENSHOT_ON_FAILURE=true python -m pytest pytests/specs --browser=chromium -q
```
