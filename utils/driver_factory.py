"""
WebDriver factory module for creating and managing browser instances
Supports Chrome, Firefox, Edge, and Safari browsers
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from utils.config import Config
import logging
import os

logger = logging.getLogger(__name__)

class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def create_driver(browser_name=None, headless=None):
        """
        Create a WebDriver instance based on browser name
        
        Args:
            browser_name (str): Browser name (chrome, firefox, edge, safari)
            headless (bool): Run browser in headless mode
            
        Returns:
            WebDriver: Selenium WebDriver instance
        """
        if browser_name is None:
            browser_name = Config.DEFAULT_BROWSER
            
        if headless is None:
            headless = Config.HEADLESS
            
        browser_name = browser_name.lower()
        logger.info(f"Creating {browser_name} driver with headless={headless}")
        
        try:
            if browser_name == 'chrome':
                return DriverFactory._create_chrome_driver(headless)
            elif browser_name == 'firefox':
                return DriverFactory._create_firefox_driver(headless)
            elif browser_name == 'edge':
                return DriverFactory._create_edge_driver(headless)
            elif browser_name == 'safari':
                return DriverFactory._create_safari_driver()
            else:
                raise ValueError(f"Unsupported browser: {browser_name}")
                
        except Exception as e:
            logger.error(f"Failed to create {browser_name} driver: {str(e)}")
            # Try alternative browser as fallback
            if browser_name == 'chrome':
                logger.info("Attempting Edge as fallback browser...")
                try:
                    return DriverFactory._create_edge_driver(headless)
                except:
                    pass
            raise
    
    @staticmethod
    def _create_chrome_driver(headless=False):
        """Create Chrome WebDriver instance"""
        options = ChromeOptions()
        
        # Get browser options from config
        browser_options = Config.get_browser_options('chrome')
        
        # Add arguments
        for arg in browser_options.get('arguments', []):
            options.add_argument(arg)
            
        # Add ESSENTIAL stability arguments to prevent Chrome crashes (REQUIRED)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        # Add SSL certificate handling for localhost
        options.add_argument('--ignore-ssl-errors-spki-list')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-certificate-errors-spki-list')
        
        # Add additional stability options for Windows
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--user-data-dir=C:\\temp\\chrome-test-profile')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-features=TranslateUI')
        options.add_argument('--disable-ipc-flooding-protection')
            
        # Add experimental options for better stability
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0,
            'profile.managed_default_content_settings.images': 2
        })
        
        # Add preferences from config
        for key, value in browser_options.get('prefs', {}).items():
            options.add_experimental_option('prefs', {key: value})
            
        if headless:
            options.add_argument('--headless')
        
        # Ensure Chrome temp directory exists
        chrome_temp_dir = "C:\\temp\\chrome-test-profile"
        os.makedirs(chrome_temp_dir, exist_ok=True)
        
        # Try to create ChromeDriver with robust error handling for corrupted binaries
        driver = None
        
        # Method 1: Try with webdriver-manager
        try:
            logger.info("Attempting ChromeDriver creation with webdriver-manager...")
            service = ChromeService(ChromeDriverManager().install())


            driver = webdriver.Chrome(service=service, options=options)




        except Exception as e:
            logger.warning(f"ChromeDriver creation failed: {e}")
            
            # Method 2: Clear cache and try fresh install
            try:
                logger.info("Clearing ChromeDriver cache and reinstalling...")
                import shutil
                cache_path = os.path.expanduser("~/.wdm/drivers/chromedriver")
                if os.path.exists(cache_path):
                    shutil.rmtree(cache_path)
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e2:
                logger.warning(f"ChromeDriver cache clear failed: {e2}")
                
                # Method 3: Try system ChromeDriver
                try:
                    logger.info("Attempting to use system ChromeDriver...")
                    driver = webdriver.Chrome(options=options)
                except Exception as e3:
                    logger.warning(f"System ChromeDriver failed: {e3}")
                    
                    # Method 4: Try with minimal options as final attempt
                    try:
                        logger.info("Attempting ChromeDriver with minimal options...")
                        minimal_options = ChromeOptions()
                        minimal_options.add_argument('--no-sandbox')
                        minimal_options.add_argument('--disable-dev-shm-usage')
                        minimal_options.add_argument('--disable-gpu')
                        minimal_options.add_argument('--remote-debugging-port=9223')
                        minimal_options.add_argument('--user-data-dir=C:\\temp\\chrome-minimal-profile')
                        os.makedirs("C:\\temp\\chrome-minimal-profile", exist_ok=True)
                        if headless:
                            minimal_options.add_argument('--headless')
                        service = ChromeService(ChromeDriverManager().install())
                        driver = webdriver.Chrome(service=service, options=minimal_options)
                    except Exception as e4:
                        logger.error(f"All ChromeDriver creation methods failed. Final error: {e4}")
                        raise Exception(f"All ChromeDriver creation methods failed. Last error: {e4}")
        
        if driver is None:
            raise Exception("Failed to create ChromeDriver - all methods exhausted")
        
        # Verify driver is working properly
        try:
            logger.info("Verifying ChromeDriver functionality...")
            driver.get("about:blank")  # Test basic navigation
            logger.info("ChromeDriver verification successful")
        except Exception as e:
            logger.error(f"ChromeDriver verification failed: {e}")
            if driver:
                driver.quit()
            raise Exception(f"ChromeDriver created but not functional: {e}")
        
        # Set implicit wait
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.maximize_window()
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless=False):
        """Create Firefox WebDriver instance"""
        options = FirefoxOptions()
        
        # Get browser options from config
        browser_options = Config.get_browser_options('firefox')
        
        # Add arguments
        for arg in browser_options.get('arguments', []):
            options.add_argument(arg)
            
        if headless:
            options.add_argument('--headless')
            
        # Use webdriver-manager to automatically manage GeckoDriver
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        # Set implicit wait
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.maximize_window()
        
        return driver
    
    @staticmethod
    def _create_edge_driver(headless=False):
        """Create Edge WebDriver instance"""
        options = EdgeOptions()
        
        # Get browser options from config
        browser_options = Config.get_browser_options('edge')
        
        # Add arguments
        for arg in browser_options.get('arguments', []):
            options.add_argument(arg)
            
        if headless:
            options.add_argument('--headless')
            
        # Use webdriver-manager to automatically manage EdgeDriver
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        # Set implicit wait
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.maximize_window()
        
        return driver
    
    @staticmethod
    def _create_safari_driver():
        """Create Safari WebDriver instance (macOS only)"""
        if os.name != 'posix':
            raise ValueError("Safari is only supported on macOS")
            
        options = SafariOptions()
        driver = webdriver.Safari(options=options)
        
        # Set implicit wait
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.maximize_window()
        
        return driver
    
    @staticmethod
    def quit_driver(driver):
        """Safely quit the WebDriver instance"""
        try:
            if driver:
                driver.quit()
                logger.info("WebDriver quit successfully")
        except Exception as e:
            logger.error(f"Error quitting WebDriver: {str(e)}")
    
    @staticmethod
    def take_screenshot(driver, file_path):
        """Take a screenshot and save it to the specified path"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Take screenshot
            driver.save_screenshot(file_path)
            logger.info(f"Screenshot saved: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return None
