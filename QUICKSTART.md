# Quick Start Guide

## Prerequisites Completed
✅ Python environment configured (Virtual Environment with Python 3.10.7)  
✅ All dependencies installed  
✅ Project structure created with Page Object Model pattern  
✅ Comprehensive test suite implemented  

## Next Steps

### 1. Update Application Configuration
Before running tests, update the configuration with your actual application details:

**File: `utils/config.py`**
- Update `BASE_URL` with your application's URL
- Adjust other settings as needed

**File: `data/test_data.json`**
- Update test URLs in the `test_urls` section
- Update valid credentials in `valid_credentials` section

### 2. Update Page Locators
After installing your application, update the locators in:

**File: `pages/login_page.py`**
- Update all locator tuples (USERNAME_INPUT, PASSWORD_INPUT, etc.) with actual element selectors from your application
- You can use browser developer tools to inspect elements and get correct selectors

### 3. Running Tests

#### Run all login tests:
```bash
.\.venv\Scripts\python.exe -m pytest tests/ -v --html=reports/report.html --self-contained-html
```

#### Run specific test categories:
```bash
# Smoke tests only
.\.venv\Scripts\python.exe -m pytest tests/ -m smoke -v

# Security tests only  
.\.venv\Scripts\python.exe -m pytest tests/ -m security -v

# Login functionality tests
.\.venv\Scripts\python.exe -m pytest tests/ -m login -v
```

#### Run with different browsers:
```bash
# Chrome (default)
.\.venv\Scripts\python.exe -m pytest tests/ --browser chrome -v

# Firefox
.\.venv\Scripts\python.exe -m pytest tests/ --browser firefox -v

# Edge
.\.venv\Scripts\python.exe -m pytest tests/ --browser edge -v

# Headless mode
.\.venv\Scripts\python.exe -m pytest tests/ --headless -v
```

### 4. Test Reports
- HTML reports are generated in the `reports/` folder
- Screenshots are taken on test failures and saved in `reports/screenshots/`
- Logs are written to `test_execution.log`

### 5. Environment Variables
Create a `.env` file based on `.env.example` to customize settings without modifying code.

## Test Coverage

The test suite includes:

1. **Positive Tests**: Valid login scenarios
2. **Negative Tests**: Invalid credentials, empty fields
3. **Security Tests**: SQL injection, XSS protection
4. **UI Tests**: Form validation, button states, keyboard navigation
5. **Edge Cases**: Multiple failed attempts, case sensitivity, special characters

## Project Structure Summary

```
auto-test/
├── pages/           # Page Object Model classes
├── tests/           # Test files and pytest configuration  
├── utils/           # Utilities (driver factory, config)
├── data/            # Test data (JSON format)
├── reports/         # Test reports and screenshots
└── .vscode/         # VS Code task configuration
```

## Support
- All locators are marked with comments indicating they need updates
- The framework is browser-agnostic and supports Chrome, Firefox, Edge, Safari
- Comprehensive logging and error handling included
- Ready for CI/CD integration
