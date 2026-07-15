# SauceDemo Test Automation Framework

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.44.0-43B02A?logo=selenium&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-9.0.3-0A9EDC?logo=pytest&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-orange)
![CI](https://github.com/AnandTenneti/SauceDemoProject/actions/workflows/ci.yml/badge.svg)

A production-grade Selenium + Pytest test automation framework for the [SauceDemo](https://www.saucedemo.com) web application, built with a **Page Object Model** architecture, multi-browser support, and an agent-based NLP command runner designed for gradual LLM integration.

**What makes this different from a typical POM demo:** most portfolio automation frameworks stop at "tests pass." This one is built around a Planner → Executor → Reporter agent pipeline that turns plain-English commands into pytest runs, deliberately kept NLP-based (spaCy/rapidfuzz) rather than LLM-dependent so it stays fast, deterministic, and free to run — with the LLM upgrade path (see [Roadmap](#roadmap)) designed in from day one rather than bolted on.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [NLP Runner](#nlp-runner)
- [Allure Reporting](#allure-reporting)
- [CI/CD](#cicd)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Overview

This framework automates end-to-end test scenarios for SauceDemo covering login, product browsing, cart management, and checkout flows. It is built to demonstrate real-world automation engineering practices including:

- **Page Object Model (POM)** for maintainability and separation of concerns
- **Multi-browser, multi-environment execution** via CLI flags
- **Parallel test execution** with `pytest-xdist`
- **Allure reporting** with automatic screenshot capture on failure
- **Agent-based NLP runner** — a Planner → Executor → Reporter pipeline that accepts natural language commands and translates them into pytest execution, architected to support LLM upgrade without structural changes

---

## Tech Stack

| Layer              | Technology                       |
| ------------------ | -------------------------------- |
| Language           | Python 3.11+                     |
| Browser Automation | Selenium WebDriver 4.44.0        |
| Test Framework     | Pytest 9.0.3                     |
| Parallel Execution | pytest-xdist 3.8.0               |
| Reporting          | Allure 2.16.0, pytest-html 4.2.0 |
| Test Data          | Faker 40.23.0                    |
| Driver Management  | webdriver-manager 4.1.2          |
| CI/CD              | GitHub Actions                   |
| Browsers           | Chrome, Firefox, Edge            |

---

## Project Structure

```
SauceDemoProject/
│
├── .github/
│   └── workflows/                  # GitHub Actions CI/CD pipeline
│
├── agents/
│   ├── planner_agent.py            # Parses user intent into execution plan
│   ├── execution_agent.py          # Builds and runs pytest command
│   ├── report_agent.py             # Generates post-run summary
│   └── execution_map.json          # Intent → pytest command mapping
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
├── tests/
│   ├── conftest.py                 # Fixtures: driver, logged_in_driver, cart_with_items
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_product_details.py
│
├── utils/
│   ├── webdriver_utils.py          # Explicit wait helpers
│   ├── common_utils.py             # File I/O, JSON helpers
│   └── test_registry.py            # Test/intent registry for the NLP runner
│
├── testdata/
│   ├── users.json                  # Test user credentials
│   ├── products.json
│   └── error_messages.json
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

Run tests on Chrome, Firefox, or Edge via a single CLI flag. Supports both local and remote Selenium Grid execution.

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

A `pytest_runtest_makereport` hook captures and attaches screenshots directly to the Allure report on any test failure — no manual step needed.

### Layered Fixtures

Fixtures compose cleanly, from raw driver to fully authenticated sessions with pre-loaded cart state:

```
driver → logged_in_driver → cart_with_items
```

### NLP Agent Runner

A three-agent pipeline (`planner_agent → execution_agent → report_agent`) accepts plain English commands and translates them to pytest execution. The architecture is deliberately designed to allow LLM integration as a drop-in upgrade to the planner layer — see [Roadmap](#roadmap).

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/AnandTenneti/SauceDemoProject.git
cd SauceDemoProject
```

**2. Create and activate a virtual environment**

```bash
# Mac/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

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

### With Allure reporting

```bash
pytest --alluredir=allure-results
allure generate allure-results --clean -o allure-report
allure open allure-report
```

---

## NLP Runner

The NLP Runner (`nlp_runner.py`) accepts plain English test commands and routes them through a Planner → Executor → Reporter pipeline.

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
ReportAgent        → Summarises results and opens Allure report
```

The pipeline uses an intent-to-command mapping (`execution_map.json`) for reliable, deterministic resolution. The agent architecture is designed so the `PlannerAgent` can be upgraded to an LLM backend without changing the `ExecutionAgent` or `ReportAgent` layers.

---

## Allure Reporting

```bash
# Run tests and collect results
pytest --alluredir=allure-results

# Generate HTML report
allure generate allure-results --clean -o allure-report

# Open in browser
allure open allure-report
```

Reports include:

- Test status by suite and marker
- Execution metadata (browser, version)
- Screenshots attached on failure
- Step-level detail per test

---

## CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that currently runs manually via `workflow_dispatch` from the Actions tab — it's not yet wired to trigger automatically on push or pull request.

Pipeline steps:

1. Set up Python environment and install Chrome
2. Install dependencies from `requirements.txt`
3. Run the test suite headlessly on Chrome (with automatic reruns on flaky failures)
4. Generate the Allure report and deploy it to GitHub Pages

---

## Roadmap

| Status  | Item                                                                    |
| ------- | ----------------------------------------------------------------------- |
| ✅ Done | Page Object Model architecture                                          |
| ✅ Done | Multi-browser support (Chrome/Firefox/Edge)                             |
| ✅ Done | Selenium Grid remote execution                                          |
| ✅ Done | Parallel execution via pytest-xdist                                     |
| ✅ Done | Allure reporting with failure screenshots                               |
| ✅ Done | NLP agent runner (Planner → Executor → Reporter)                        |
| ✅ Done | GitHub Actions CI pipeline                                              |
| 🔜 Next | Tiered locator fallback (DOM heuristics → LLM)                          |
| 🔜 Next | LLM-powered planner agent (Claude / OpenAI)                             |
| 🔜 Next | Self-healing locators (auto-update execution_map.json from LLM results) |
| 🔜 Next | Slack / email report notifications                                      |
| 🔜 Next | Docker Compose for local Selenium Grid                                  |

---

## Author

**Anand Kiran Tenneti**
Senior Automation Engineer

[![GitHub](https://img.shields.io/badge/GitHub-AnandTenneti-181717?logo=github)](https://github.com/AnandTenneti)