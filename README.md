# AI-Powered Enterprise QA Automation & Self-Healing Test Platform

A Python-based test automation framework for web UI and API testing, built around Selenium WebDriver, PyTest, and the Page Object Model.

## Project Overview

This project demonstrates maintainable test automation, reusable framework components, failure diagnostics, and continuous integration using the OrangeHRM public demo application as the UI test target.

The API test layer uses a separately configured mock API where appropriate. It is not presented as a production integration with OrangeHRM.

## Technology Stack

- Python
- Selenium WebDriver
- PyTest
- Page Object Model (POM)
- Requests for API testing
- Faker for test data
- Allure PyTest integration
- pytest-xdist for parallel execution
- GitHub Actions
- JSON-based failure and flaky-test analysis

## Architecture

- `Framework/driver/` — WebDriver creation and browser configuration
- `Framework/pages/` — Page Object Model classes
- `Framework/api/` — Reusable API client
- `Framework/ai/` — Failure analysis, approved locator fallbacks, and flaky-test analysis
- `Framework/utils/` — Shared waits, logging, and screenshot utilities
- `tests/` — Organized test suites
- `test_data/` — Test data generation and fixtures
- `config/` — Environment-based configuration
- `.github/workflows/` — CI workflow definitions

## Key Capabilities

- Reusable UI automation using Page Objects
- Explicit waits and centralized browser setup
- UI and API test execution with PyTest
- Screenshots and diagnostics for failed tests
- Rule-based failure classification
- Configurable locator fallback experiments
- Historical pass/fail outcome analysis
- Allure result collection and JUnit reporting
- CI execution through GitHub Actions
- Parallel execution for suitable independent tests

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Configure environment variables using `.env.example` as a reference.
4. Ensure browser and driver prerequisites are available.
5. Run the relevant tests using the commands below.

Do not commit credentials, tokens, or environment files containing secrets.

## Run Tests

Run the full suite:

`pytest`

Run smoke tests:

`pytest -m smoke`

Run API tests:

`pytest -m api`

Run unit tests:

`pytest -m unit`

Run independent tests in parallel:

`pytest -n 2 -m "api or unit"`

Generate Allure results:

`pytest --alluredir=reports/allure-results`

Generate JUnit XML:

`pytest --junitxml=reports/junit.xml`

## AI and Self-Healing Scope

Failure classification currently uses rules and regular expressions. Locator recovery uses explicitly configured fallback locators. Flaky-test analysis identifies mixed pass/fail outcomes in supplied test history.

These are diagnostic and recovery mechanisms, not proof of autonomous AI reasoning. A fallback locator must be validated before interacting with an element.

## CI/CD

GitHub Actions can execute the configured test suite on pushes and pull requests. Test results and available diagnostics are uploaded as workflow artifacts.

See `.github/workflows/tests.yml` for the pipeline configuration.


## Limitations

- The public demo may change, become unavailable, or reset test data.
- Demo credentials and application behavior are not under this project's control.
- Mock API tests do not establish integration with the OrangeHRM backend.
- Locator fallbacks require explicit validation.
- Flaky-test detection requires historical outcomes and does not independently establish root cause.


## Disclaimer

This is a learning and portfolio project intended for authorized testing of public demo applications and test APIs.
