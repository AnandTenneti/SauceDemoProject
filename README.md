# SauceDemoProject

A production-grade Selenium/pytest automation framework for [SauceDemo](https://www.saucedemo.com), built with the **Page Object Model** pattern. Features self-healing locators, parallel execution, Allure reporting, and an AI-driven test runner powered by Claude.

---

## Features

- **Page Object Model** — clean separation of page interactions from test logic
- **Self-healing locators** — multi-locator fallback strategy in `BasePage` automatically tries alternative selectors before failing
- **AI test runner** — natural language interface to plan, execute, and report tests via `ai_runner.py`
- **Parallel execution** — pytest-xdist with 4 workers (`-n 4`) out of the box
- **Cross-browser support** — Chrome, Firefox, and Edge (headless and headed)
- **Data-driven testing** — JSON-based test data for users and error messages
- **Allure + HTML reporting** — rich reports with screenshots on failure
- **Faker integration** — reproducible synthetic test data via seeded Faker

---

## Project Structure

```
SauceDemoProject/
├── agents/                     # AI agent layer
│   ├── planner_agent.py        # Parses natural language → test plan
│   ├── execution_agent.py      # Executes pytest commands
│   └── report_agent.py         # Generates and opens Allure reports
│
├── config/
│   ├── config.py               # Loads settings.json
│   └── settings.json           # Base URL and timeout config
│
├── pages/                      # Page Object Model classes
│   ├── BasePage.py             # Base class with self-healing find_element_with_fallback
│   ├── LoginPage.py
│   ├── HomePage.py
│   ├── CartPage.py
│   ├── CheckoutPage.py
│   ├── HeaderPage.py
│   └── ProductDetailsPage.py
│
├── runners/
│   └── run_cross_browser.py    # Cross-browser smoke run (Chrome + Firefox)
│
├── testdata/
│   ├── users.json              # Valid user credentials
│   └── error_messages.json     # Invalid users and expected error messages
│
├── tests/
│   ├── conftest.py             # Fixtures: driver, logged_in_driver, cart_with_items, fake
│   ├── test_login.py           # 6 login tests (smoke + regression)
│   ├── test_inventory.py       # 3 inventory/sort tests
│   ├── test_cart.py            # 2 cart tests
│   └── test_checkout.py        # 2 checkout tests
│
├── utils/
│   ├── common_utils.py         # File I/O and shared helpers
│   ├── webdriver_utils.py      # WebDriverWait wrappers
│   └── test_registry.py        # Reads markers from pytest.ini for AI runner
│
├── ai_runner.py                # Interactive AI-powered test runner
├── pytest.ini                  # Pytest config, markers, parallel settings
└── requirements.txt
```

---

## Installation

**Prerequisites:** Python 3.10+, Google Chrome / Firefox / Edge installed.

```bash
# Clone the repo
git clone https://github.com/AnandTenneti/SauceDemoProject.git
cd SauceDemoProject

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running Tests

### Run the full suite

```bash
pytest
```

### Run by marker

```bash
pytest -m smoke
pytest -m regression
pytest -m login
pytest -m checkout
pytest -m inventory
pytest -m cart
```

### Run on a specific browser

```bash
pytest --browser=chrome
pytest --browser=firefox
pytest --browser=edge
```

### Run on a specific browser with a marker

```bash
pytest -m smoke --browser=firefox
```

### Run cross-browser smoke tests

```bash
python runners/run_cross_browser.py
```

---

## Reporting

### Allure report

```bash
pytest --alluredir=allure-results
allure generate allure-results --clean -o allure-report
allure open allure-report
```

### HTML report

```bash
pytest --html=reports/report.html
```

Screenshots are automatically captured on test failure and attached to the Allure report.

---

## AI Runner

An interactive natural language interface for running tests:

```bash
python ai_runner.py
```

**Example prompts:**

```
What tests should I run? → run smoke tests on chrome
What tests should I run? → run login and checkout regression tests on firefox with allure
What tests should I run? → run all tests on chrome and firefox
What tests should I run? → quit
```

The AI runner parses the request, builds the appropriate `pytest` command, executes it, and optionally generates an Allure report.

---

## Configuration

**`config/settings.json`**

```json
{
  "base_url": "https://www.saucedemo.com/",
  "timeout": 10
}
```

**`testdata/users.json`** — credentials used by `logged_in_driver` fixture and login tests.

---

## Key Design Decisions

### Self-healing locators

`BasePage.find_element_with_fallback` accepts either a single locator tuple or a list of fallback tuples. It tries each in order and raises an informative error only if all fail:

```python
__USERNAME_INPUT = [
    (By.ID, "user-name"),
    (By.NAME, "user-name"),
    (By.CSS_SELECTOR, "[data-test='username']")
]
```

### Fixtures

| Fixture            | Scope    | Description                                           |
| ------------------ | -------- | ----------------------------------------------------- |
| `driver`           | function | Fresh browser instance per test                       |
| `logged_in_driver` | function | Driver pre-logged-in as `standard_user`               |
| `cart_with_items`  | function | Logged-in driver with 3 items in cart                 |
| `fake`             | function | Seeded Faker instance (seed=42) for reproducible data |

### Parallel execution

Tests run across 4 workers by default (`addopts = -n 4` in `pytest.ini`). All fixtures are function-scoped to ensure worker isolation.

---

## Markers

| Marker       | Description                                |
| ------------ | ------------------------------------------ |
| `smoke`      | Core happy-path tests — run on every build |
| `regression` | Full regression suite                      |
| `sanity`     | Quick sanity checks                        |
| `login`      | Login-related tests                        |
| `checkout`   | Checkout flow tests                        |
| `inventory`  | Inventory/product page tests               |
| `cart`       | Cart management tests                      |

---

## Dependencies

| Package           | Version | Purpose                     |
| ----------------- | ------- | --------------------------- |
| selenium          | 4.44.0  | Browser automation          |
| pytest            | 9.0.3   | Test framework              |
| pytest-xdist      | 3.8.0   | Parallel execution          |
| pytest-html       | 4.2.0   | HTML reporting              |
| allure-pytest     | 2.16.0  | Allure reporting            |
| Faker             | 40.23.0 | Test data generation        |
| webdriver-manager | 4.1.2   | Automatic driver management |

---

## Author

**Anand Tenneti** — Senior Automation Engineer  
GitHub: [@AnandTenneti](https://github.com/AnandTenneti)
