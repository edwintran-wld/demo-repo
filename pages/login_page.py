"""
Login page object model
Contains all elements and methods related to login functionality
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Login page object containing login-related elements and methods"""
    
    # Locators - Updated for common login patterns
    # Primary locators (try these first)
    NAME_INPUT = (By.XPATH, '//*[@name="fullname"]')
    USERNAME_INPUT = (By.XPATH, '//input[@name="username"]')
    EMAIL_INPUT = (By.XPATH, '//*[@name="email"]')
    PASSWORD_INPUT = (By.XPATH, '//input[@type="password"]')
    LOGIN_BUTTON = (By.XPATH, '//*[@id="augmentedButton-1047"]')
    REMEMBER_ME_CHECKBOX = (By.XPATH, '//*[@id="ext-gen1197"]')
    FORGOT_PASSWORD_LINK = (By.XPATH, '//*[@id="simpleLink-1046"]')
    NOTIFICATION_MESSAGE = (By.XPATH, '//*[@id="ext-gen1174"]')
    PRODUCT_LOGO = (By.XPATH, '//*[@id="productLogoView-1021"]')
    LOGOUT_BUTTON = (By.XPATH, '//*[@id="ext-gen1929"]')
    LOGOUT_SECOND_BUTTON = (By.XPATH, '//*[@id="simpleLink-1486"]')
    

    
    def __init__(self, driver):
        """
        Initialize login page
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
    
    def is_element_present(self, locator):
        """
        Check if element is present without throwing exception
        
        Args:
            locator (tuple): Element locator
            
        Returns:
            bool: True if element exists, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except Exception:
            return False
    


    def navigate_to_login_page(self):
        """Navigate to the login page"""
        try:
            from utils.config import Config
            login_url = f"{Config.BASE_URL}/c/login"  # Updated with actual login URL
            self.navigate_to(login_url)
            logger.info("Navigated to login page")
        except Exception as e:
            logger.error(f"Failed to navigate to login page: {str(e)}")
            raise
    
    def enter_username(self, username):
        """
        Enter username in the username field
        
        Args:
            username (str): Username to enter
        """
        try:
            element = self.find_element(self.USERNAME_INPUT)
            element.clear()
            element.send_keys(username)
            logger.info(f"Entered username: {username}")
        except Exception as e:
            logger.error(f"Failed to enter username: {str(e)}")
            raise
    
    def enter_password(self, password):
        """
        Enter password in the password field
        
        Args:
            password (str): Password to enter
        """
        try:
            element = self.find_element(self.PASSWORD_INPUT)
            element.clear()
            element.send_keys(password)
            logger.info("Entered password")
        except Exception as e:
            logger.error(f"Failed to enter password: {str(e)}")
            raise
    
    def click_login_button(self):
        """Click the login button"""
        try:
            element = self.find_element(self.LOGIN_BUTTON)
            element.click()
            logger.info("Clicked login button")
        except Exception as e:
            logger.error(f"Failed to click login button: {str(e)}")
            raise
    
    def click_remember_me(self):
        """Click the remember me checkbox if it exists"""
        try:
            if self.is_element_present(self.REMEMBER_ME_CHECKBOX):
                self.click_element(self.REMEMBER_ME_CHECKBOX)
                logger.info("Clicked remember me checkbox")
            else:
                logger.warning("Remember me checkbox not found")
        except Exception as e:
            logger.warning(f"Could not click remember me checkbox: {e}")
    
    def click_forgot_password(self):
        """Click the forgot password link if it exists"""
        try:
            if self.is_element_present(self.FORGOT_PASSWORD_LINK):
                self.click_element(self.FORGOT_PASSWORD_LINK)
                logger.info("Clicked forgot password link")
            else:
                logger.warning("Forgot password link not found")
        except Exception as e:
            logger.warning(f"Could not click forgot password link: {e}")
    
    def get_error_message(self):
        """
        Get notification message text
        
        Returns:
            str: Notification message text
        """
        try:
            element = self.find_element(self.NOTIFICATION_MESSAGE)
            message_text = element.text
            logger.info(f"Notification message found: {message_text}")
            return message_text
        except Exception as e:
            logger.info("No notification message found")
            return ""
    
    def get_success_message(self):
        """
        Get success message text
        
        Returns:
            str: Success message text
        """
        try:
            success_text = self.get_text(self.SUCCESS_MESSAGE)
            logger.info(f"Success message found: {success_text}")
            return success_text
        except Exception as e:
            logger.info("No success message found")
            return ""
    
    def is_error_message_displayed(self):
        """
        Check if notification/error message is displayed
        Uses multiple strategies to detect error messages
        
        Returns:
            bool: True if any error message is visible, False otherwise
        """
        try:
            # Strategy 1: Check the primary notification message element
            if self.is_element_present(self.NOTIFICATION_MESSAGE):
                element = self.find_element(self.NOTIFICATION_MESSAGE)
                if element.is_displayed() and element.text.strip():
                    return True
            
            # Strategy 2: Look for common error message patterns
            error_patterns = [
                "//div[contains(@class, 'error')]",
                "//div[contains(@class, 'alert')]", 
                "//span[contains(@class, 'error')]",
                "//*[contains(text(), 'Invalid')]",
                "//*[contains(text(), 'incorrect')]",
                "//*[contains(text(), 'failed')]"
            ]
            
            for pattern in error_patterns:
                try:
                    elements = self.driver.find_elements(By.XPATH, pattern)
                    for element in elements:
                        if element.is_displayed() and element.text.strip():
                            return True
                except Exception:
                    continue
                    
            return False
        except Exception:
            return False
    
    def is_success_message_displayed(self):
        """
        Check if success message is displayed (same as notification message)
        
        Returns:
            bool: True if success message is visible, False otherwise
        """
        try:
            element = self.find_element(self.NOTIFICATION_MESSAGE)
            message_text = element.text.strip().lower()
            # Check for success indicators in the message
            success_keywords = ['success', 'welcome', 'login successful', 'logged in']
            return element.is_displayed() and any(keyword in message_text for keyword in success_keywords)
        except Exception:
            return False
    
    def is_login_button_enabled(self):
        """
        Check if login button is enabled
        
        Returns:
            bool: True if login button is enabled, False otherwise
        """
        try:
            button = self.find_element(self.LOGIN_BUTTON)
            return button.is_enabled()
        except Exception as e:
            logger.error(f"Failed to check login button status: {str(e)}")
            return False
    
    def is_remember_me_checked(self):
        """
        Check if remember me checkbox is checked
        
        Returns:
            bool: True if checkbox is checked, False otherwise
        """
        try:
            checkbox = self.find_element(self.REMEMBER_ME_CHECKBOX)
            return checkbox.is_selected()
        except Exception as e:
            logger.error(f"Failed to check remember me status: {str(e)}")
            return False
    
    def is_password_field_masked(self):
        """
        Check if password field is properly masked
        
        Returns:
            bool: True if password field type is 'password', False otherwise
        """
        try:
            element = self.find_element(self.PASSWORD_INPUT)
            field_type = element.get_attribute("type")
            return field_type == "password"
        except Exception as e:
            logger.error(f"Failed to check password field masking: {str(e)}")
            return False
    
    def login(self, username, password, remember_me=False):
        """
        Perform complete login action
        
        Args:
            username (str): Username
            password (str): Password
            remember_me (bool): Whether to check remember me option
            
        Returns:
            bool: True if login successful (PRODUCT_LOGO is visible), False otherwise
        """
        logger.info(f"Attempting login with username: {username}")
        
        self.enter_username(username)
        self.enter_password(password)
        
        if remember_me:
            self.click_remember_me()
            
        self.click_login_button()
        
        # Wait a moment for the page to process the login
        import time
        time.sleep(2)
        
        # Check if login was successful by looking for PRODUCT_LOGO
        try:
            self.wait_for_element_visible(self.PRODUCT_LOGO, timeout=10)
            logger.info("Login successful - PRODUCT_LOGO is visible")
            return True
        except Exception as e:
            logger.error(f"Login failed - PRODUCT_LOGO not found: {str(e)}")
            return False
    
    def logout(self):
        """
        Perform 2-step logout action
        
        Returns:
            bool: True if logout successful (Username input is visible), False otherwise
        """
        try:
            # Step 1: Click the first logout button
            first_logout_element = self.find_element(self.LOGOUT_BUTTON)
            first_logout_element.click()
            logger.info("Clicked first logout button")
            
            # Wait for the second logout button to appear
            import time
            time.sleep(2)
            
            # Step 2: Click the second logout button
            second_logout_element = self.wait_for_element_visible(self.LOGOUT_SECOND_BUTTON, timeout=10)
            second_logout_element.click()
            logger.info("Clicked second logout button")
            
            # Check if logout was successful by looking for username input
            try:
                self.wait_for_element_visible(self.USERNAME_INPUT, timeout=10)
                logger.info("Logout successful - Username input is visible")
                return True
            except Exception as e:
                logger.error(f"Logout verification failed - Username input not found: {str(e)}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to logout: {str(e)}")
            return False
    
    def clear_login_form(self):
        """Clear all login form fields"""
        try:
            username_element = self.find_element(self.USERNAME_INPUT)
            username_element.clear()
            
            password_element = self.find_element(self.PASSWORD_INPUT)
            password_element.clear()
            
            logger.info("Cleared login form")
        except Exception as e:
            logger.error(f"Failed to clear login form: {str(e)}")
            raise
    
    def get_username_field_value(self):
        """
        Get current value of username field
        
        Returns:
            str: Username field value
        """
        try:
            element = self.find_element(self.USERNAME_INPUT)
            return element.get_attribute("value")
        except Exception as e:
            logger.error(f"Failed to get username field value: {str(e)}")
            return ""
    
    def get_password_field_value(self):
        """
        Get current value of password field
        
        Returns:
            str: Password field value
        """
        try:
            element = self.find_element(self.PASSWORD_INPUT)
            return element.get_attribute("value")
        except Exception as e:
            logger.error(f"Failed to get password field value: {str(e)}")
            return ""
    
    def is_login_form_displayed(self):
        """
        Check if login form is displayed
        
        Returns:
            bool: True if all login form elements are visible
        """
        try:
            username_element = self.find_element(self.USERNAME_INPUT)
            password_element = self.find_element(self.PASSWORD_INPUT)
            login_element = self.find_element(self.LOGIN_BUTTON)
            
            return (username_element.is_displayed() and 
                    password_element.is_displayed() and 
                    login_element.is_displayed())
        except Exception:
            return False
    
    def wait_for_login_form(self, timeout=10):
        """
        Wait for login form to be displayed
        
        Args:
            timeout (int): Wait timeout in seconds
        """
        try:
            # Wait for each element to be available
            self.wait_for_element_present(self.USERNAME_INPUT, timeout)
            self.wait_for_element_present(self.PASSWORD_INPUT, timeout) 
            self.wait_for_element_present(self.LOGIN_BUTTON, timeout)
            logger.info("Login form is displayed")
        except Exception as e:
            logger.error(f"Login form not found within {timeout} seconds: {str(e)}")
            raise
    
    def is_logged_in(self):
        """
        Check if user is successfully logged in by looking for PRODUCT_LOGO
        
        Returns:
            bool: True if logged in successfully (PRODUCT_LOGO is visible)
        """
        try:
            # Check if PRODUCT_LOGO is visible to confirm login success
            product_logo_element = self.find_element(self.PRODUCT_LOGO)
            is_logged_in = product_logo_element.is_displayed()
            logger.info(f"Login status check: {'Logged in' if is_logged_in else 'Not logged in'}")
            return is_logged_in
            
        except Exception as e:
            logger.error(f"Failed to check login status - PRODUCT_LOGO not found: {str(e)}")
            return False
    
    def press_key_on_username(self, key):
        """Press a key on the username field"""
        try:
            element = self.find_element(self.USERNAME_INPUT)
            element.send_keys(key)
            logger.info(f"Pressed key {key} on username field")
        except Exception as e:
            logger.error(f"Failed to press key {key} on username field: {str(e)}")
            raise
    
    def press_key_on_password(self, key):
        """Press a key on the password field"""
        try:
            element = self.find_element(self.PASSWORD_INPUT)
            element.send_keys(key)
            logger.info(f"Pressed key {key} on password field")
        except Exception as e:
            logger.error(f"Failed to press key {key} on password field: {str(e)}")
            raise
