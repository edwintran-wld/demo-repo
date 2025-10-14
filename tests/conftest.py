"""
Pytest configuration and fixtures
Contains shared fixtures and test setup/teardown logic
"""

import pytest
import json
import os
import logging
from datetime import datetime
from utils.driver_factory import DriverFactory
from utils.config import Config
from pages.login_page import LoginPage

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """Add command line options for pytest"""
    parser.addoption(
        "--browser", 
        action="store", 
        default=Config.DEFAULT_BROWSER,
        help="Browser to run tests on: chrome, firefox, edge, safari"
    )
    parser.addoption(
        "--headless", 
        action="store_true",
        default=Config.HEADLESS,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=Config.BASE_URL,
        help="Base URL for the application under test"
    )

@pytest.fixture(scope="session")
def browser_name(request):
    """Get browser name from command line option"""
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def headless_mode(request):
    """Get headless mode from command line option"""
    return request.config.getoption("--headless")

@pytest.fixture(scope="session")
def base_url(request):
    """Get base URL from command line option"""
    return request.config.getoption("--base-url")

@pytest.fixture(scope="function")
def driver(browser_name, headless_mode):
    """
    Create WebDriver instance for each test
    
    Args:
        browser_name (str): Browser name from command line
        headless_mode (bool): Headless mode from command line
        
    Yields:
        WebDriver: Selenium WebDriver instance
    """
    logger.info(f"Setting up {browser_name} driver (headless={headless_mode})")
    
    driver_instance = None
    try:
        driver_instance = DriverFactory.create_driver(browser_name, headless_mode)
        yield driver_instance
    except Exception as e:
        logger.error(f"Failed to create driver: {str(e)}")
        raise
    finally:
        if driver_instance:
            # Take screenshot on failure
            test_name = os.environ.get('PYTEST_CURRENT_TEST', 'unknown_test')
            screenshot_path = os.path.join(
                Config.SCREENSHOT_PATH, 
                f"{test_name.split('::')[-1]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            DriverFactory.take_screenshot(driver_instance, screenshot_path)
            
            # Quit driver
            DriverFactory.quit_driver(driver_instance)
            logger.info("Driver cleanup completed")

@pytest.fixture(scope="function")
def login_page(driver):
    """
    Create LoginPage instance for each test
    
    Args:
        driver: WebDriver instance
        
    Returns:
        LoginPage: Login page object
    """
    return LoginPage(driver)

@pytest.fixture(scope="session")
def test_data():
    """
    Load test data from JSON file
    
    Returns:
        dict: Test data dictionary
    """
    try:
        with open(Config.TEST_DATA_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info("Test data loaded successfully")
            return data
    except FileNotFoundError:
        logger.error(f"Test data file not found: {Config.TEST_DATA_PATH}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in test data file: {str(e)}")
        raise

@pytest.fixture(scope="function")
def valid_credentials(test_data):
    """
    Get valid login credentials
    
    Args:
        test_data (dict): Test data dictionary
        
    Returns:
        dict: Valid credentials
    """
    return test_data["valid_credentials"]

@pytest.fixture(scope="function")
def invalid_credentials(test_data):
    """
    Get invalid login credentials list
    
    Args:
        test_data (dict): Test data dictionary
        
    Returns:
        list: List of invalid credentials
    """
    return test_data["invalid_credentials"]

@pytest.fixture(scope="function")
def empty_field_tests(test_data):
    """
    Get empty field test cases
    
    Args:
        test_data (dict): Test data dictionary
        
    Returns:
        list: List of empty field test cases
    """
    return test_data["empty_field_tests"]

@pytest.fixture(scope="function")
def sql_injection_tests(test_data):
    """
    Get SQL injection test cases
    
    Args:
        test_data (dict): Test data dictionary
        
    Returns:
        list: List of SQL injection test cases
    """
    return test_data["sql_injection_tests"]

@pytest.fixture(scope="function")
def xss_tests(test_data):
    """
    Get XSS test cases
    
    Args:
        test_data (dict): Test data dictionary
        
    Returns:
        list: List of XSS test cases
    """
    return test_data["xss_tests"]

@pytest.fixture(autouse=True)
def setup_test_environment(request):
    """
    Setup test environment before each test
    This fixture runs automatically before each test
    """
    # Set current test name in environment for screenshot naming
    os.environ['PYTEST_CURRENT_TEST'] = request.node.nodeid
    
    # Create reports directory if it doesn't exist
    os.makedirs(Config.REPORTS_PATH, exist_ok=True)
    os.makedirs(Config.SCREENSHOT_PATH, exist_ok=True)
    
    logger.info(f"Starting test: {request.node.nodeid}")
    
    yield
    
    logger.info(f"Completed test: {request.node.nodeid}")

@pytest.fixture(scope="function")
def login_and_navigate(login_page, base_url):
    """
    Navigate to login page before test
    
    Args:
        login_page (LoginPage): Login page object
        base_url (str): Base URL for the application
    """
    login_page.navigate_to_login_page()
    login_page.wait_for_login_form()

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "login: mark test as login functionality test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as security test"
    )

def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    if call.when == "call":
        if call.excinfo is not None:
            # Test failed, screenshot should be taken in driver fixture cleanup
            logger.error(f"Test failed: {item.nodeid}")
        else:
            logger.info(f"Test passed: {item.nodeid}")

def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Login Automation Test Report"

def pytest_html_results_summary(prefix, summary, postfix):
    """Customize HTML report summary"""
    prefix.extend([
        "<h2>Test Environment Information</h2>",
        f"<p>Base URL: {Config.BASE_URL}</p>",
        f"<p>Browser: {Config.DEFAULT_BROWSER}</p>",
        f"<p>Headless Mode: {Config.HEADLESS}</p>",
        f"<p>Test Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
    ])
