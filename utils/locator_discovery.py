"""
Locator Discovery Utility
This utility helps discover and update locators for the login page
Run this after the application is accessible to get the correct selectors
"""

from selenium.webdriver.common.by import By
from utils.driver_factory import DriverFactory
from utils.config import Config
import json
import time

class LocatorDiscovery:
    """Utility class to discover and suggest locators for login elements"""
    
    def __init__(self):
        self.driver = None
        self.discovered_locators = {}
    
    def start_discovery(self, url=None):
        """Start the locator discovery process"""
        if url is None:
            url = f"{Config.BASE_URL}/c/main"
            
        try:
            self.driver = DriverFactory.create_driver('chrome', headless=False)
            self.driver.get(url)
            time.sleep(3)
            
            print(f"Page loaded: {self.driver.title}")
            print(f"URL: {self.driver.current_url}")
            
            # Discover elements
            self.discover_username_field()
            self.discover_password_field()
            self.discover_login_button()
            self.discover_error_messages()
            self.discover_other_elements()
            
            # Generate locator suggestions
            self.generate_locator_suggestions()
            
            return self.discovered_locators
            
        except Exception as e:
            print(f"Discovery failed: {e}")
            return None
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def discover_username_field(self):
        """Discover username/email input field"""
        selectors = [
            ("input[type='text']", "text inputs"),
            ("input[type='email']", "email inputs"),
            ("input[name*='user']", "username-like inputs"),
            ("input[name*='email']", "email-like inputs"),
            ("input[placeholder*='user']", "username placeholder"),
            ("input[placeholder*='email']", "email placeholder"),
        ]
        
        self.discovered_locators['username'] = self._discover_element(selectors, "Username Field")
    
    def discover_password_field(self):
        """Discover password input field"""
        selectors = [
            ("input[type='password']", "password inputs"),
            ("input[name*='pass']", "password-like inputs"),
            ("input[placeholder*='pass']", "password placeholder"),
        ]
        
        self.discovered_locators['password'] = self._discover_element(selectors, "Password Field")
    
    def discover_login_button(self):
        """Discover login/submit button"""
        selectors = [
            ("button[type='submit']", "submit buttons"),
            ("input[type='submit']", "submit inputs"),
            ("button:contains('Login')", "login text buttons"),
            ("button:contains('Sign In')", "sign in buttons"),
            ("[role='button']", "role buttons"),
        ]
        
        self.discovered_locators['login_button'] = self._discover_element(selectors, "Login Button")
    
    def discover_error_messages(self):
        """Discover error message containers"""
        selectors = [
            ("[class*='error']", "error class elements"),
            ("[class*='alert']", "alert elements"),
            ("[role='alert']", "alert role elements"),
            ("[class*='message']", "message elements"),
        ]
        
        self.discovered_locators['error_message'] = self._discover_element(selectors, "Error Message")
    
    def discover_other_elements(self):
        """Discover other common login elements"""
        # Remember me checkbox
        remember_selectors = [
            ("input[type='checkbox']", "checkboxes"),
            ("[name*='remember']", "remember elements"),
            ("[id*='remember']", "remember ID elements"),
        ]
        self.discovered_locators['remember_me'] = self._discover_element(remember_selectors, "Remember Me")
        
        # Forgot password link
        forgot_selectors = [
            ("a[href*='forgot']", "forgot password links"),
            ("a[href*='reset']", "reset password links"),
            ("a:contains('Forgot')", "forgot text links"),
        ]
        self.discovered_locators['forgot_password'] = self._discover_element(forgot_selectors, "Forgot Password")
    
    def _discover_element(self, selectors, element_name):
        """Discover element using multiple selectors"""
        found_elements = []
        
        print(f"\nSearching for {element_name}...")
        
        for selector, description in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    element_info = {
                        'selector': selector,
                        'description': description,
                        'tag': element.tag_name,
                        'id': element.get_attribute('id'),
                        'name': element.get_attribute('name'),
                        'class': element.get_attribute('class'),
                        'type': element.get_attribute('type'),
                        'placeholder': element.get_attribute('placeholder'),
                        'text': element.text[:50] if element.text else '',
                        'visible': element.is_displayed(),
                        'enabled': element.is_enabled()
                    }
                    
                    # Generate locator suggestions
                    locator_suggestions = []
                    if element_info['id']:
                        locator_suggestions.append(f"(By.ID, '{element_info['id']}')")
                    if element_info['name']:
                        locator_suggestions.append(f"(By.NAME, '{element_info['name']}')")
                    if element_info['class']:
                        classes = element_info['class'].split()
                        for cls in classes:
                            locator_suggestions.append(f"(By.CLASS_NAME, '{cls}')")
                    
                    locator_suggestions.append(f"(By.CSS_SELECTOR, '{selector}')")
                    
                    element_info['suggested_locators'] = locator_suggestions
                    found_elements.append(element_info)
                    
                    print(f"  Found: {element_info['tag']} - ID: {element_info['id']}, Name: {element_info['name']}")
                    
            except Exception as e:
                print(f"  Error with selector '{selector}': {e}")
        
        return found_elements
    
    def generate_locator_suggestions(self):
        """Generate Python code suggestions for locators"""
        print("\n" + "="*50)
        print("LOCATOR SUGGESTIONS FOR LOGIN_PAGE.PY")
        print("="*50)
        
        for element_type, elements in self.discovered_locators.items():
            if elements:
                print(f"\n# {element_type.upper()} LOCATORS:")
                best_element = elements[0]  # Take the first found element
                
                if best_element['suggested_locators']:
                    primary_locator = best_element['suggested_locators'][0]
                    print(f"    {element_type.upper()}_INPUT = {primary_locator}")
                    
                    if len(best_element['suggested_locators']) > 1:
                        print(f"    # Alternative locators:")
                        for alt_locator in best_element['suggested_locators'][1:]:
                            print(f"    # {element_type.upper()}_INPUT = {alt_locator}")
        
        # Save detailed results
        with open('locator_discovery_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.discovered_locators, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed results saved to: locator_discovery_results.json")

def run_discovery():
    """Run the locator discovery process"""
    discovery = LocatorDiscovery()
    results = discovery.start_discovery()
    
    if results:
        print("\nDiscovery completed successfully!")
        print("Use the generated suggestions to update your login_page.py file.")
    else:
        print("Discovery failed. Please check if the application is running and accessible.")

if __name__ == "__main__":
    run_discovery()
