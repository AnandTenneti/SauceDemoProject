# SauceDemo Test Automation Framework

## Overview

This project is a Selenium + Pytest automation framework built for testing the SauceDemo application.

The framework follows the Page Object Model (POM) design pattern and includes:

- Selenium WebDriver
- Pytest
- Allure Reporting
- Cross-browser execution
- AI-powered test execution runner
- Utility libraries for reusable actions
- Page Object Model architecture

---

## Tech Stack

- Python 3.x
- Selenium WebDriver
- Pytest
- Allure Reports
- Pytest-Xdist
- ChromeDriver / FirefoxDriver / EdgeDriver

---

## Project Structure

```text
project/
│
├── agents/
│   ├── planner_agent.py
│   ├── execution_agent.py
│   ├── report_agent.py
│   └── execution_map.json
│
├── pages/
│   ├── BasePage.py
│   ├── LoginPage.py
│   ├── HomePage.py
│   ├── CartPage.py
│   ├── CheckoutPage.py
│   └── HeaderPage.py
│
├── tests/
│   ├── test_login.py
│   ├── test_home.py
│   ├── test_cart.py
│   └── test_checkout.py
│
├── utils/
│   ├── webdriver_utils.py
│   ├── common_utils.py
│   └── logger.py
│
├── allure-results/
├── allure-report/
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── ai_runner.py
```

---

## Features

### Test Execution

- Smoke Suite
- Regression Suite
- Full Test Suite Execution

### Browser Support

- Chrome
- Firefox
- Edge

### Reporting

- Allure Reports
- Screenshots on failure
- Execution summaries

### AI Runner

The framework includes an AI-powered runner that interprets natural language commands and executes tests.

Examples:

```text
Run smoke tests
Run regression tests on chrome
Run smoke and regression tests on firefox
Run all tests on edge with allure report
```

---

## Installation

Clone repository:

```bash
git clone <repository-url>
cd saucedemo
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Tests

### Smoke Tests

```bash
pytest -m smoke
```

### Regression Tests

```bash
pytest -m regression
```

### Run All Tests

```bash
pytest
```

### Cross Browser Execution

```bash
pytest --browser=chrome
pytest --browser=firefox
pytest --browser=edge
```

---

## Allure Reporting

Generate results:

```bash
pytest --alluredir=allure-results
```

Generate report:

```bash
allure generate allure-results --clean -o allure-report
```

Open report:

```bash
allure open allure-report
```

---

## AI Runner

Start the AI Runner:

```bash
python ai_runner.py
```

Example commands:

```text
Run smoke tests
Run regression tests on chrome
Run smoke and regression tests on firefox
Run all tests on edge with allure report
```

The AI Runner:

1. Understands user intent.
2. Creates an execution plan.
3. Builds the pytest command.
4. Executes tests.
5. Generates Allure reports.

---

## Test Design Pattern

The framework follows the Page Object Model (POM).

Benefits:

- Improved maintainability
- Reduced code duplication
- Better readability
- Easier scalability

---

## Reporting & Logging

- Allure Reports
- Failure screenshots
- Execution logs
- Detailed test steps

---

## Future Enhancements

- OpenAI-powered execution planning
- Parallel execution
- Environment selection (QA/UAT/Prod)
- Emailing reports
- Slack notifications
- Docker integration
- CI/CD integration using GitHub Actions/Jenkins

---

## Author

Anand Kiran

Automation Test Engineer
