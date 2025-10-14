"""
Configuration module for test automation framework
Contains all configuration settings and constants
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class containing all test settings"""
    
    # Application settings
    BASE_URL = os.getenv('BASE_URL', 'https://localhost:4443')
    
    # Browser settings
    DEFAULT_BROWSER = os.getenv('BROWSER', 'firefox')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    
    # Test data settings
    TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.json')
    
    # Report settings
    REPORTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'reports')
    SCREENSHOT_PATH = os.path.join(REPORTS_PATH, 'screenshots')
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Security test settings
    SQL_INJECTION_PAYLOADS = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users --"
    ]
    
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "javascript:alert('XSS')",
        "<img src=x onerror=alert('XSS')>"
    ]
    
    @classmethod
    def get_browser_options(cls, browser_name):
        """Get browser-specific options"""
        options = {
            'chrome': {
                'arguments': [
                    '--disable-extensions',
                    '--disable-gpu',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ],
                'prefs': {
                    'profile.default_content_setting_values.notifications': 2
                }
            },
            'firefox': {
                'arguments': [
                    '--disable-extensions',
                    '--disable-gpu'
                ]
            },
            'edge': {
                'arguments': [
                    '--disable-extensions',
                    '--disable-gpu'
                ]
            }
        }
        
        if cls.HEADLESS:
            options[browser_name]['arguments'].append('--headless')
            
        return options.get(browser_name.lower(), {})
