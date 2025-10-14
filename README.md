# Login Automation Test Suite

This project contains automated test cases for validating login functionality using Selenium WebDriver and Python with Page Object Model (POM) pattern. The framework is designed to be resilient and adaptable to different web application behaviors.

## Project Structure

```
auto-test/
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   └── conftest.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── login_page.py
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py
│   └── config.py
├── data/
│   └── test_data.json
├── reports/
│   └── .gitkeep
├── requirements.txt
├── pytest.ini
└── README.md
```

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page elements
- **Resilient Test Logic**: Adaptive tests that handle different application behaviors
- **Multi-Strategy Element Detection**: Multiple fallback methods for finding elements
- **Selenium WebDriver**: Cross-browser automation with enhanced stability
- **pytest**: Advanced testing framework with fixtures and comprehensive reporting
- **JSON Configuration**: Externalized test data and configuration
- **HTML Reports**: Detailed test execution reports with screenshots
- **Cross-browser Testing**: Support for Chrome, Firefox (default), Edge, and Safari
- **SSL Certificate Handling**: Built-in support for localhost HTTPS applications

## Installation

1. Install Python 3.8 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The test suite is configured via `utils/config.py`:

- **Base URL**: `https://localhost:4443` (configurable via BASE_URL environment variable)
- **Default Browser**: Firefox (configurable via BROWSER environment variable)
- **Timeouts**: Implicit wait (10s), Explicit wait (20s)
- **Test Data**: Located in `data/test_data.json`

Environment variables can be set in a `.env` file or system environment.

## Running Tests

### Basic Commands

Execute all tests:
```bash
pytest tests/ -v
```

Execute specific test file:
```bash
pytest tests/test_login.py -v
```

Execute specific test:
```bash
pytest tests/test_login.py::TestLogin::test_valid_login -v
```

### With HTML Report
```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Browser-Specific Testing
```bash
# Firefox (default)
pytest tests/ --browser=firefox -v

# Chrome
pytest tests/ --browser=chrome -v

# Edge
pytest tests/ --browser=edge -v

# Headless mode
pytest tests/ --headless -v
```

### Test Categories
```bash
# Run only smoke tests
pytest -m smoke -v

# Run only security tests  
pytest -m security -v

# Run only login tests
pytest -m login -v
```

## Test Data

Test data is stored in `data/test_data.json` and includes:
- Valid login credentials
- Invalid login credentials
- Edge cases for login validation

## Browser Support

- **Firefox (default)**: Recommended for most testing scenarios
- **Chrome**: Full support with enhanced stability options
- **Edge**: Cross-platform support
- **Safari**: macOS only

The framework includes robust WebDriver management with automatic fallback mechanisms and enhanced stability options for Chrome on Windows systems.

## Test Cases Covered

### ✅ **Login Functionality**
1. **Valid Login**: Successful login with correct credentials (verifies PRODUCT_LOGO visibility)
2. **Invalid Credentials**: Multiple invalid username/password combinations
3. **Empty Fields**: Username empty, password empty, both empty
4. **Login Button State**: Button enablement and interaction
5. **2-Step Logout Process**: Complete logout workflow with verification

### 🔒 **Security Testing**
6. **SQL Injection Protection**: Various SQL injection payload attempts
7. **XSS Protection**: Cross-site scripting prevention validation
8. **Multiple Failed Attempts**: Account lockout and rate limiting behavior
9. **Password Field Masking**: Ensures password type='password' attribute

### 🎛️ **UI/UX Validation** 
10. **Remember Me Functionality**: Checkbox interaction (if available)
11. **Forgot Password Link**: Navigation validation (if available)
12. **Keyboard Navigation**: Tab order and Enter key functionality
13. **Form Validation**: Client-side and server-side validation
14. **Page Refresh During Login**: Session handling validation

### 🔍 **Adaptive Testing Features**
- **Multi-Strategy Error Detection**: Finds error messages using multiple approaches
- **Optional Element Handling**: Gracefully skips tests for missing UI elements
- **Flexible Validation Logic**: Adapts to different application error handling patterns
- **Robust Element Finding**: Multiple locator strategies with intelligent fallbacks

## Current Status

✅ **Framework Complete**: Fully functional test automation framework  
✅ **Locators Updated**: DOM-specific XPath locators implemented  
✅ **SSL Handling**: Configured for https://localhost:4443 applications  
✅ **Resilient Tests**: Adaptive logic handles various application behaviors  
✅ **WebDriver Stability**: Enhanced Chrome/Firefox driver management  
✅ **2-Step Logout**: Implemented complete logout workflow  
✅ **Error Detection**: Multi-strategy error message detection  

## Quick Start

1. **Verify Configuration**: Check `utils/config.py` settings
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Run Single Test**: `pytest tests/test_login.py::TestLogin::test_valid_login -v`
4. **Run Full Suite**: `pytest tests/ -v --html=reports/report.html --self-contained-html`
5. **View Results**: Open `reports/report.html` in your browser

## Troubleshooting

### WebDriver Issues
If you encounter WebDriver crashes or SSL certificate errors:
```bash
# Use Firefox (more stable for localhost)
pytest tests/ --browser=firefox -v

# Run in headless mode
pytest tests/ --headless -v
```

### Missing Elements
Tests automatically adapt to missing UI elements (Remember Me, Forgot Password) by:
- Checking element existence before interaction
- Skipping tests gracefully when elements are unavailable  
- Using multiple detection strategies for error messages

## Technical Notes

### WebDriver Management
- **Automatic Binary Management**: webdriver-manager handles browser drivers
- **Enhanced Stability**: Chrome includes Windows-specific crash prevention options
- **SSL Certificate Handling**: Configured for localhost HTTPS applications
- **Fallback Mechanisms**: Automatic browser switching if primary driver fails

### Test Resilience Features
- **Multi-Strategy Error Detection**: Combines CSS selectors, XPath patterns, and text matching
- **Graceful Element Handling**: Tests skip when optional elements (Remember Me, Forgot Password) are missing
- **Adaptive Validation Logic**: Handles applications that don't show error messages by checking login state
- **Robust Locators**: Direct DOM element targeting with comprehensive error handling

### Data Security
- **Environment Variables**: Sensitive configuration via .env files
- **JSON Test Data**: Externalized credentials and test scenarios  
- **Screenshot Security**: Automatic screenshot capture on test failures
- **Credential Management**: Separate valid/invalid credential sets

### Framework Architecture
```
BasePage (base_page.py)
├── Common WebDriver operations
├── Element interaction methods  
├── Wait strategies
└── Screenshot capabilities

LoginPage (login_page.py) 
├── Inherits from BasePage
├── Login-specific locators
├── 2-step logout implementation
└── Multi-strategy error detection

Test Classes (test_login.py)
├── TestLogin: Core login functionality
├── TestLogout: Logout workflow testing
└── Adaptive assertion logic
```

This framework is production-ready and handles real-world application variability! 🚀
