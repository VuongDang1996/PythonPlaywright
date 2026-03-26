# Python Playwright Framework (Pytest + POM + Allure)

This repository is a Python-first end-to-end test automation framework for Automation Exercise, built on Playwright, Pytest, Page Object Model, and Allure reporting.

## Current Framework Scope

- Python 3.12 test stack (Playwright + Pytest)
- Page Object Model with component-based composition
- Typed runtime settings from environment variables
- Parallel execution with pytest-xdist
- Allure raw results and HTML report generation
- JUnit summary and flaky-trend scripts for CI insights
- Behave BDD execution with tag-aware CI runs
- GitHub Actions pipelines for PR, main, nightly, and manual runs

## Tech Stack

- playwright
- pytest
- pytest-playwright
- allure-pytest
- pytest-rerunfailures
- pytest-xdist
- python-dotenv
- behave (BDD support)
- ruff, black, mypy (quality gates)

## Project Structure

```text
.
|-- pytests/
|   |-- config/                # Typed settings and environment parsing
|   |-- components/            # Reusable UI components
|   |-- pages/                 # Page objects
|   |-- data/                  # Test data and factories
|   |-- specs/                 # Test scenarios
|   |-- utils/                 # Cross-cutting helpers
|   |-- conftest.py            # Fixtures and hooks
|   `-- ARCHITECTURE.md        # Layering and dependency rules
|-- features/                  # Behave BDD features
|-- scripts/
|   |-- summarize_junit.py     # JUnit -> summary markdown/json
|   `-- update_flaky_trend.py  # Trend tracking for flaky/pass-rate
|-- .github/workflows/
|   |-- python-pytest.yml
|   |-- python-pytest-nightly.yml
|   |-- manual.yml
|   `-- individual-tests.yml   # Legacy TypeScript workflow
|-- requirements.txt
|-- requirements-dev.txt
|-- pytest.ini
|-- pyproject.toml
|-- PYTHON_FRAMEWORK_RUN_GUIDE.md
`-- README.md
```

## Installation

1. Clone repository

```bash
git clone https://github.com/VuongDang1996/PythonPlaywright.git
cd PythonPlaywright
```

2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

3. Install Playwright browser(s)

```bash
python -m playwright install chromium
```

For Linux CI environments, the workflows use:

```bash
python -m playwright install --with-deps chromium
```

## Environment Configuration

Create .env from .env.example and set at least:

```env
BASE_URL=https://automationexercise.com
HEADLESS=true
DEFAULT_TIMEOUT_MS=30000
NAVIGATION_TIMEOUT_MS=60000
AE_VALID_USER_EMAIL=your-valid-user@example.com
AE_VALID_USER_PASSWORD=your-valid-password
```

## Run Tests Locally

Run full suite:

```bash
python -m pytest pytests/specs --browser=chromium -q
```

Run smoke only:

```bash
python -m pytest pytests/specs --browser=chromium -m smoke -q
```

Run regression only:

```bash
python -m pytest pytests/specs --browser=chromium -m regression -q
```

Run single test file:

```bash
python -m pytest pytests/specs/automation_exercise/individual_tests/test_tc01_register_user.py --browser=chromium -q
```

Run in headed mode:

```bash
python -m pytest pytests/specs --browser=chromium --headed -q
```

Collect tests only:

```bash
python -m pytest --collect-only pytests/specs -q
```

Run from a suite file (similar to Selenium TestNG XML):

```bash
python scripts/run_test_suite.py --suite test-suites/cross-browser.json
```

Run TC01 on Edge using suite file:

```bash
python scripts/run_test_suite.py --suite test-suites/tc01-edge.json
```

Run Behave BDD scenarios:

```bash
python -m behave features
python -m behave features --tags @smoke
python -m behave features --dry-run
python -m behave features --junit --junit-directory test-results/behave-junit
```

## Suite File Guideline (Like Selenium TestNG XML)

Use JSON files in `test-suites/` to control what runs, what is skipped, which browsers are used, and how parallel execution is configured.

### 1. Create or choose a suite file

- Existing examples:
  - `test-suites/scenario-00-simple-firefox.json`
  - `test-suites/scenario-02-smoke-cross-browser.json`
  - `test-suites/scenario-08-edge-auth-batch.json`

### 2. Run by suite file

```bash
python scripts/run_test_suite.py --suite test-suites/scenario-00-simple-firefox.json
```

### 3. Suite file fields

- `description`: Human-readable suite name.
- `paths`: Test files/folders to include.
- `exclude_paths`: Paths to skip using `--ignore`.
- `markers`: Marker filter expression, for example `smoke and not quarantine`.
- `keyword`: `-k` expression for test name filtering.
- `browsers`: Browser list, for example `chromium`, `firefox`, `webkit`.
- `browser_channel`: Optional channel for Chromium, for example `msedge` or `chrome`.
- `workers`: Worker count for xdist (`1`, `2`, `4`, `auto`).
- `headed`: `true` to show browser UI, `false` for headless.
- `quiet`: `true` to run with `-q`.
- `maxfail`: Stop early after N failures.
- `allure_dir`: Allure raw output folder.
- `junit_xml`: JUnit XML output path.
- `extra_args`: Any additional pytest args.

### 4. Minimal suite example

```json
{
  "description": "Simple one-test run on Firefox",
  "paths": [
    "pytests/specs/automation_exercise/individual_tests/test_tc01_register_user.py"
  ],
  "browsers": [
    "firefox"
  ],
  "workers": "1",
  "quiet": true,
  "junit_xml": "test-results/junit-simple.xml"
}
```

### 5. Typical use cases

- Smoke validation across browsers.
- Edge-only batch for auth flows.
- Fast local debugging with one file and `headed=true`.
- Nightly regression using markers + workers + retries in `extra_args`.

Notes:
- pytest.ini already enables parallel execution by default with -n auto and --dist=loadscope.
- To limit concurrency, pass a fixed worker count such as -n 4.

## Quality Checks

```bash
python -m ruff check pytests/config pytests/components pytests/pages pytests/data pytests/conftest.py
python -m black --check pytests/config pytests/components pytests/pages pytests/data pytests/conftest.py
python -m mypy pytests/config pytests/components pytests/pages pytests/data pytests/conftest.py
```

## Reporting

Run with Allure raw results:

```bash
python -m pytest pytests/specs --browser=chromium --alluredir=allure-results -q
```

Generate Allure HTML:

```bash
allure generate allure-results --clean -o allure-report
```

Open report:

```bash
allure open allure-report
```

Generate JUnit XML:

```bash
python -m pytest pytests/specs --browser=chromium --junitxml=test-results/junit-python.xml -q
```

Generate CI-style summaries:

```bash
python scripts/summarize_junit.py --input test-results/junit-python.xml --output-json test-results/summary.json --output-md test-results/summary.md --title "Local Python Summary"
python scripts/update_flaky_trend.py --summary-json test-results/summary.json --trend-file test-results/flaky-trend.json --output-json test-results/flaky-trend.json --output-md test-results/flaky-trend.md --run-id local --run-number 1 --workflow local --ref local --sha local --browser chromium --event manual
```

CI triage flow (recommended order):

1. Open the GitHub job summary and check the latest Python summary table (failed/error split, pass rate, and duration).
2. Read the Flaky Trend section for status (improved, flat, mixed, regressed) and delta vs previous run.
3. Download `python-pytest-metrics-*` or `python-nightly-metrics-*` artifacts for `summary.md`, `summary.json`, and `flaky-trend.json` details.
4. Open the Allure artifact (or GitHub Pages report on main) for step-level traces and screenshots.
5. Download `behave-bdd-results-*` for BDD command output (`behave-output.txt`) and BDD JUnit/summary files.

## GitHub Actions Workflows

Primary Python workflows:

- .github/workflows/python-pytest.yml
  - PR/main validation pipeline
  - quality gates
  - parallel pytest
  - Behave BDD job (`test-behave`) with tag expression support (`@smoke` on PR, full on push by default)
  - Allure artifact and optional Pages publish
  - JUnit summary and flaky trend artifacts

- .github/workflows/python-pytest-nightly.yml
  - nightly matrix run (chromium, firefox, webkit)
  - retries for stability
  - combined nightly Allure publish

- .github/workflows/manual.yml
  - manual Python pytest dispatch
  - browser choice: chromium/firefox/webkit/all
  - optional upload to self-hosted Allure TestOps when secrets are configured

Legacy workflow:

- .github/workflows/individual-tests.yml remains for the older TypeScript path and is not the primary Python pipeline.

## Optional: Self-Hosted Allure TestOps Integration

The CI workflows now support optional upload of raw Allure results to a self-hosted Allure TestOps instance.

Required GitHub repository secrets:

- ALLURE_TESTOPS_ENDPOINT
- ALLURE_TESTOPS_TOKEN
- ALLURE_TESTOPS_PROJECT_ID

Optional rollout toggle secret:

- ALLURE_TESTOPS_ENABLED (`true` by default when unset, set to `false` to disable uploads without editing workflows)

Optional CI quality gate secrets (used in primary and nightly Python workflows):

- QUALITY_GATE_ENABLED (`false` by default)
- QUALITY_GATE_MIN_PASS_RATE (`95` by default)
- QUALITY_GATE_MAX_FAILED_TOTAL (`0` by default)
- QUALITY_GATE_MAX_FLAKY (`5` by default)

Quality gate outputs:

- `test-results/quality-gate.md` is generated in the primary workflow.
- `test-results/<browser>/quality-gate.md` is generated in nightly matrix jobs.
- Primary PR comments include the quality gate section when available.

Behavior:

- If all three secrets are set, workflows install `allurectl` and upload raw results.
- If any secret is missing, uploads are skipped automatically.
- Upload steps are non-blocking (`continue-on-error: true`) to avoid breaking existing CI.

Current workflows with optional upload support:

- .github/workflows/python-pytest.yml
- .github/workflows/python-pytest-nightly.yml
- .github/workflows/manual.yml
- .github/workflows/individual-tests.yml

## NPM Convenience Scripts

package.json includes helper scripts that call Python commands, for example:

```bash
npm test
npm run py:test
npm run py:test:smoke
npm run py:test:parallel
npm run py:test:suite
npm run py:test:suite:tc01:edge
npm run py:test:allure
```

## Documentation

- [PYTHON_FRAMEWORK_RUN_GUIDE.md](PYTHON_FRAMEWORK_RUN_GUIDE.md)
- [pytests/ARCHITECTURE.md](pytests/ARCHITECTURE.md)
- [AUTOMATION_EXERCISE_GUIDE.md](AUTOMATION_EXERCISE_GUIDE.md)
- [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md)
- [CUCUMBER_GUIDE.md](CUCUMBER_GUIDE.md)

## Contributing

1. Create a feature branch.
2. Keep selectors inside pages/components, not specs.
3. Run quality checks and test collection locally.
4. Update docs when behavior or commands change.

## License

MIT
