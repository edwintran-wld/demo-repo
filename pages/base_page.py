"""
Base page module containing common page functionality
All page objects should inherit from this base class
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.config import Config
import logging
import time

logger = logging.getLogger(__name__)

class BasePage:
    """Base page class containing common page functionality"""
    
    def __init__(self, driver):
        """
        Initialize base page
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
    
    def navigate_to(self, url):
        """
        Navigate to a specific URL
        
        Args:
            url (str): URL to navigate to
        """
        try:
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            self.wait_for_page_load()
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Element locator (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
            
        Returns:
            WebElement: The located element
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element {locator} is visible")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not visible after {timeout} seconds")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Element locator (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
            
        Returns:
            WebElement: The located element
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            logger.debug(f"Element {locator} is clickable")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not clickable after {timeout} seconds")
            raise
    
    def wait_for_element_present(self, locator, timeout=None):
        """
        Wait for element to be present in DOM (not necessarily visible)
        
        Args:
            locator (tuple): Element locator (By.ID, 'element_id')
            timeout (int): Wait timeout in seconds
            
        Returns:
            WebElement: The located element
        """
        if timeout is None:
            timeout = Config.EXPLICIT_WAIT
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Element {locator} is present")
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not present after {timeout} seconds")
            raise
    
    def find_element(self, locator):
        """
        Find element using locator
        
        Args:
            locator (tuple): Element locator (By.ID, 'element_id')
            
        Returns:
            WebElement: The located element
        """
        try:
            element = self.driver.find_element(*locator)
            logger.debug(f"Element {locator} found")
            return element
        except NoSuchElementException:
            logger.error(f"Element {locator} not found")
            raise
    
    def find_elements(self, locator):
        """
        Find multiple elements using locator
        
        Args:
            locator (tuple): Element locator (By.CLASS_NAME, 'class_name')
            
        Returns:
            list: List of WebElements
        """
        try:
            elements = self.driver.find_elements(*locator)
            logger.debug(f"Found {len(elements)} elements with locator {locator}")
            return elements
        except Exception as e:
            logger.error(f"Error finding elements {locator}: {str(e)}")
            raise
    
    def click_element(self, locator, timeout=None):
        """
        Click on element
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout in seconds
        """
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            element.click()
            logger.info(f"Clicked element {locator}")
        except Exception as e:
            logger.error(f"Failed to click element {locator}: {str(e)}")
            raise
    
    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """
        Enter text into an input field
        
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
            clear_first (bool): Clear field before entering text
            timeout (int): Wait timeout in seconds
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Entered text '{text}' into element {locator}")
        except Exception as e:
            logger.error(f"Failed to enter text into element {locator}: {str(e)}")
            raise
    
    def get_text(self, locator, timeout=None):
        """
        Get text from element
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout in seconds
            
        Returns:
            str: Element text
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            text = element.text
            logger.debug(f"Got text '{text}' from element {locator}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        """
        Get attribute value from element
        
        Args:
            locator (tuple): Element locator
            attribute_name (str): Attribute name
            timeout (int): Wait timeout in seconds
            
        Returns:
            str: Attribute value
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            value = element.get_attribute(attribute_name)
            logger.debug(f"Got attribute '{attribute_name}' = '{value}' from element {locator}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute '{attribute_name}' from element {locator}: {str(e)}")
            raise
    
    def is_element_present(self, locator):
        """
        Check if element is present on the page
        
        Args:
            locator (tuple): Element locator
            
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Element locator
            timeout (int): Wait timeout in seconds
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_load(self, timeout=30):
        """
        Wait for page to load completely
        
        Args:
            timeout (int): Wait timeout in seconds
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.debug("Page loaded completely")
        except TimeoutException:
            logger.warning(f"Page did not load completely within {timeout} seconds")
    
    def scroll_to_element(self, locator):
        """
        Scroll to element
        
        Args:
            locator (tuple): Element locator
        """
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            logger.debug(f"Scrolled to element {locator}")
        except Exception as e:
            logger.error(f"Failed to scroll to element {locator}: {str(e)}")
            raise
    
    def get_current_url(self):
        """
        Get current page URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def get_page_title(self):
        """
        Get current page title
        
        Returns:
            str: Page title
        """
        return self.driver.title
    
    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()
        self.wait_for_page_load()
        logger.info("Page refreshed")
    
    def press_key(self, locator, key, timeout=None):
        """
        Press a key on an element
        
        Args:
            locator (tuple): Element locator
            key: Key to press (from Keys class)
            timeout (int): Wait timeout in seconds
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            element.send_keys(key)
            logger.info(f"Pressed key {key} on element {locator}")
        except Exception as e:
            logger.error(f"Failed to press key {key} on element {locator}: {str(e)}")
            raise
