# SauceDemo Test Automation Framework

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.44.0-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-9.0.3-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-Report-orange)](https://anandtenneti.github.io/SauceDemoProject/)
[![CI](https://github.com/AnandTenneti/SauceDemoProject/actions/workflows/ci.yml/badge.svg)](https://github.com/AnandTenneti/SauceDemoProject/actions/workflows/ci.yml)

A Selenium + Pytest test automation framework for the [SauceDemo](https://www.saucedemo.com) web application. It combines a **Page Object Model** architecture, multi-browser and parallel execution, cookie-seeded sessions, and a **Planner → Executor → Reporter** agent pipeline that turns plain-English commands into pytest runs.

**[Live Allure report](https://anandtenneti.github.io/SauceDemoProject/)** · [CI runs](https://github.com/AnandTenneti/SauceDemoProject/actions) · [Design decisions](#design-decisions) · [Roadmap](#roadmap)

**What makes this different from a typical POM demo:** most portfolio frameworks stop at "tests pass." This one adds an agent-based runner that is deliberately deterministic (rule-based, not LLM-dependent) so it stays fast, free to run, and predictable, with an LLM upgrade path designed in from day one rather than bolted on.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Overview](#overview)
- [Design Decisions](#design-decisions)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Test Coverage](#test-coverage)
- [Running Tests](#running-tests)
- [NLP Runner](#nlp-runner)
- [Allure Reporting](#allure-reporting)
- [CI/CD](#cicd)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Quick Start

**Prerequisites:** Python 3.11+ and Google Chrome. The Allure CLI (which needs Java) is only required if you want to view reports locally.

```bash
git clone https://github.com/AnandTenneti/SauceDemoProject.git
cd SauceDemoProject

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
pytest -m smoke
```

---

## Overview

This framework automates end-to-end scenarios for SauceDemo covering login, product browsing, product details, cart management, and checkout. It demonstrates real-world automation engineering practices:

- **Page Object Model (POM)** for maintainability and separation of concerns
- **Multi-browser, multi-environment execution** via CLI flags (Chrome, Firefox, Edge; local or Selenium Grid)
- **Parallel execution** with `pytest-xdist`
- **Session seeding** that skips the login UI for tests that don't test login
- **Allure reporting** with automatic screenshot capture on failure
- **Two-tier CI**: fast smoke checks on every push/PR and a nightly full regression with a published Allure report
- **Agent-based NLP runner** that accepts natural-language commands, architected so an LLM backend can be swapped in without structural changes

---

## Design Decisions

The trade-offs behind the framework, and why each call was made.

| Decision | Why |
| --- | --- |
| **Cookie-injection session seeding** | Only login tests should pay for the login UI. Every other test starts authenticated via the `seeded_driver` fixture, which injects SauceDemo's `session-username` cookie directly. |
| **Cart set up through the UI, not localStorage** | Seeding cart state via localStorage was evaluated and rejected: SauceDemo's Angular app holds cart state in memory and doesn't persist it reliably. |
| **Rule-based planner instead of an LLM** | Deterministic, fast, and free to run. `PlannerAgent` sits behind a clean interface, so an LLM backend can replace it without touching `ExecutionAgent` or `ReportAgent`. |
| **NLP kept local and lightweight** | The runner is deliberately not wired to an LLM API. LLM integration is deferred to a future release. |
| **Smoke on every push/PR, full regression nightly** | Quick feedback on changes without giving up full coverage and a published Allure history. |
| **Explicit waits inside `BasePage` lookups** | `find_element_with_fallback` and `find_elements` wrap `WebDriverWait` (`presence_of_element_located`) to remove intermittent `NoSuchElementException` and silent zero-count reads right after navigations and clicks. |
| **Collection check in CI** | `pytest --collect-only -q` runs before browser setup so structural and collection errors fail fast. |

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3.11+ |
| Browser automation | Selenium WebDriver |
| Test framework | Pytest, `pytest-xdist` (parallel), `pytest-rerunfailures` (flaky reruns) |
| Reporting | Allure, `pytest-html`, coverage |
| Test data | Faker, JSON fixtures |
| Driver management | `webdriver-manager` |
| CI/CD | GitHub Actions, GitHub Pages |
| Browsers | Chrome, Firefox, Edge |

Exact dependency versions are pinned in [`requirements.txt`](requirements.txt).

---

## Project Structure

```
SauceDemoProject/
│
├── .github/
│   └── workflows/                  # GitHub Actions CI/CD pipeline (ci.yml)
│
├── agents/
│   ├── planner_agent.py            # Parses user intent into an execution plan
│   ├── execution_agent.py          # Builds and runs the pytest command
│   └── report_agent.py             # Generates the post-run summary
│
├── config/
│   ├── config.py                   # Environment/browser configuration
│   └── settings.json
│
├── pages/
│   ├── BasePage.py                 # Base class with shared WebDriver utilities
│   ├── LoginPage.py
│   ├── HomePage.py
│   ├── CartPage.py
│   ├── CheckoutPage.py
│   ├── HeaderPage.py
│   └── ProductDetailsPage.py
│
├── runners/                        # Runner support modules
│
├── tests/
│   ├── conftest.py                 # Fixtures: driver, logged_in_driver, seeded_driver, cart_with_items
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_product_details.py
│
├── utils/
│   ├── webdriver_utils.py          # Explicit wait helpers
│   ├── common_utils.py             # File I/O, JSON helpers
│   ├── test_registry.py            # Reads markers from pytest.ini for the NLP runner
│   └── session_seeder.py           # Cookie-injection session seeding (bypasses login UI)
│
├── testdata/
│   ├── users.json                  # Test user credentials
│   ├── products.json
│   └── error_messages.json
│
├── nlp_runner.py                   # NLP command runner entry point
├── pytest.ini                      # Markers, test paths, CLI defaults
├── requirements.txt
└── README.md
```

---

## Features

### Page Object Model

Each page is encapsulated in its own class inheriting from `BasePage`, keeping locators and actions separate from test logic.

### Multi-Browser Support

Run tests on Chrome, Firefox, or Edge with a single CLI flag. Supports both local and remote Selenium Grid execution.

```bash
pytest --browser=chrome
pytest --browser=firefox --env=remote
```

### Parallel Execution

Tests are `pytest-xdist` compatible. Run the full suite across multiple workers:

```bash
pytest -n auto
```

### Screenshot on Failure

A `pytest_runtest_makereport` hook captures and attaches screenshots directly to the Allure report on any test failure, with no manual step needed.

### Layered Fixtures

Fixtures compose cleanly, from a raw driver up to a pre-loaded cart:

```
driver → logged_in_driver                  (drives the real login form, for tests that verify login/logout itself)
driver → seeded_driver → cart_with_items   (cookie-seeded session, for tests that just need to be logged in)
```

### Session State Seeding

`logged_in_driver` exercises the actual login form, which is correct for tests that verify login behavior but wasteful for every other test that merely needs an authenticated session. `SessionSeeder` (`utils/session_seeder.py`) seeds an authenticated session by injecting SauceDemo's `session-username` cookie directly, skipping the login UI. It is used through the `seeded_driver` fixture.

Cart state, by contrast, is held in the Angular app's in-memory component state rather than reliably persisted, so injecting it the same way was evaluated and rejected. Cart setup still goes through the UI (`cart_with_items`).

### Tiered Locator Fallback

Locator resolution is designed as three tiers, from cheapest to most flexible:

1. **Tier 1: intent mapping.** Look up the element from a known intent.
2. **Tier 2: DOM heuristics.** `FallbackLocator` inspects the DOM when the primary locator fails.
3. **Tier 3: LLM.** Deferred to a future release (see [Roadmap](#roadmap)).

### NLP Agent Runner

A three-agent pipeline (`planner_agent → execution_agent → report_agent`) accepts plain-English commands and translates them into pytest execution. See [NLP Runner](#nlp-runner).

---

## Test Coverage

| Suite | File | Covers |
| --- | --- | --- |
| Login | `test_login.py` | Authentication flows and error messages, driven through the real login form |
| Inventory | `test_inventory.py` | Product listing and browsing |
| Product details | `test_product_details.py` | Individual product pages |
| Cart | `test_cart.py` | Adding single and multiple items, cart persistence across page refresh and re-login |
| Checkout | `test_checkout.py` | Checkout flow |

Tests are tagged with `smoke` and `regression` markers (defined in `pytest.ini`), which drive both local runs and the CI split.

---

## Running Tests

### By marker

```bash
pytest -m smoke                     # Smoke suite
pytest -m regression                # Regression suite
pytest -m "smoke or regression"     # Combined
pytest                              # All tests
```

### By browser

```bash
pytest --browser=chrome             # Default
pytest --browser=firefox
pytest --browser=edge
```

### With parallel execution

```bash
pytest -n auto                      # Auto-detect workers
pytest -n 4                         # 4 workers
```

### Remote execution (Selenium Grid)

```bash
pytest --env=remote --browser=chrome
```

---

## NLP Runner

The NLP Runner (`nlp_runner.py`) accepts plain-English test commands and routes them through a Planner → Executor → Reporter pipeline.

**Start the runner:**

```bash
python nlp_runner.py
```

**Example commands:**

```
Run smoke tests
Run regression tests on chrome
Run smoke and regression tests on firefox
Run all tests on edge with allure report
```

**How it works:**

```
User Command
     │
     ▼
PlannerAgent       → Parses intent, extracts browser/suite/options
     │
     ▼
ExecutionAgent     → Builds and runs the pytest command
     │
     ▼
ReportAgent        → Summarises results and opens the Allure report
```

`PlannerAgent` resolves intent deterministically. It reads the live marker list from `pytest.ini` (via `utils/test_registry.py`) and regex-matches it, along with browser names and flags like "parallel" or "allure", against the free-text request, including simple negation ("regression but not checkout"). No LLM or fuzzy-matching library is involved yet.

The agent architecture is designed so `PlannerAgent` can be upgraded to an LLM backend later without changing `ExecutionAgent` or `ReportAgent`.

---

## Allure Reporting

Generate and open a report locally (requires the [Allure CLI](https://allurereport.org/docs/install/)):

```bash
pytest --alluredir=allure-results
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Reports include:

- Test status by suite and marker
- Execution metadata (browser, version)
- Screenshots attached on failure
- Step-level detail per test

The nightly CI run publishes the latest report to GitHub Pages: **[view the live report](https://anandtenneti.github.io/SauceDemoProject/)**.

---

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yml`) is split into two jobs:

| Job | Trigger | What it runs |
| --- | --- | --- |
| `smoke` | Automatically on every push/PR to `main` | `-m smoke` tests headlessly on Chrome, with coverage and Allure results uploaded as artifacts |
| `regression` | Nightly (`02:00 UTC` cron) or manual `workflow_dispatch` | Full test suite with coverage, then deploys the Allure report to GitHub Pages |

Both jobs install dependencies from `requirements.txt`, run a fast collection check (`pytest --collect-only -q`), install Chrome, rerun flaky failures automatically, and upload a coverage report as a build artifact. Only the nightly/manual `regression` job generates and publishes the Allure history to GitHub Pages.

---

## Roadmap

| Status | Item |
| --- | --- |
| ✅ Done | Page Object Model architecture |
| ✅ Done | Multi-browser support (Chrome/Firefox/Edge) |
| ✅ Done | Selenium Grid remote execution |
| ✅ Done | Parallel execution via pytest-xdist |
| ✅ Done | Allure reporting with failure screenshots |
| ✅ Done | NLP agent runner (Planner → Executor → Reporter) |
| ✅ Done | GitHub Actions CI split into smoke (push/PR) and nightly/manual regression jobs |
| ✅ Done | Allure report published to GitHub Pages |
| ✅ Done | Cookie-injection session seeding to bypass the login UI for non-login tests |
| ✅ Done | DOM-heuristic locator fallback (`FallbackLocator`) |
| 🔜 Next | Data-driven test coverage expansion |
| 🔜 Next | Tier 3 locator fallback (LLM) |
| 🔜 Next | LLM-powered planner agent (Claude / OpenAI) |
| 🔜 Next | Slack / email report notifications |
| 🔜 Next | Docker Compose for a local Selenium Grid |

---

## Author

**Anand Kiran Tenneti**, Senior Automation Engineer. 18+ years in QA and 10+ years in test automation across Selenium, Playwright, and REST Assured, including enterprise client work.

[![GitHub](https://img.shields.io/badge/GitHub-AnandTenneti-181717?logo=github)](https://github.com/AnandTenneti)

<!-- Add a LinkedIn badge/link or contact email here -->