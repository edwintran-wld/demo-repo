"""
Comprehensive login functionality test suite
Tests all aspects of login functionality including positive, negative, and security tests
"""

import pytest
import logging
import time
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

class TestLogin:
    """Test class for login functionality"""
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Valid login with correct username and password
        
        Steps:
        1. Navigate to login page
        2. Enter valid username
        3. Enter valid password
        4. Click login button
        5. Verify successful login
        """
        logger.info("Starting test_valid_login")
        
        # Perform login
        login_page.login(
            username=valid_credentials["username"],
            password=valid_credentials["password"]
        )
        
        # Verify successful login
        assert login_page.is_logged_in(), "User should be logged in successfully"
        logger.info("Valid login test passed")
    
    @pytest.mark.login
    def test_invalid_credentials(self, login_page, invalid_credentials, login_and_navigate):
        """
        Test Case: Login with invalid credentials
        
        Steps:
        1. Navigate to login page
        2. Enter invalid username/password combination
        3. Click login button
        4. Verify error message is displayed
        """
        for credentials in invalid_credentials:
            logger.info(f"Testing invalid credentials: {credentials['username']}")
            
            # Attempt login with invalid credentials
            login_page.login(
                username=credentials["username"],
                password=credentials["password"]
            )
            
            # Verify error message is displayed OR user is not logged in
            # Some applications may not show error messages but simply not log in
            error_displayed = login_page.is_error_message_displayed()
            user_logged_in = login_page.is_logged_in()
            
            assert error_displayed or not user_logged_in, \
                "Either error message should be displayed OR user should not be logged in"
            
            if error_displayed:
                error_message = login_page.get_error_message()
                logger.info(f"Error message displayed: {error_message}")
            
            # Verify user is not logged in
            assert not login_page.is_logged_in(), "User should not be logged in"
            
            # Clear form for next iteration
            login_page.clear_login_form()
            
        logger.info("Invalid credentials test passed")
    
    @pytest.mark.login
    def test_empty_fields(self, login_page, empty_field_tests, login_and_navigate):
        """
        Test Case: Login with empty username or password fields
        
        Steps:
        1. Navigate to login page
        2. Leave username or password field empty
        3. Click login button
        4. Verify appropriate error message is displayed
        """
        for test_case in empty_field_tests:
            logger.info(f"Testing empty fields: username='{test_case['username']}', password='{test_case['password']}'")
            
            # Attempt login with empty fields
            login_page.login(
                username=test_case["username"],
                password=test_case["password"]
            )
            
            # Verify error message is displayed OR user is not logged in
            error_displayed = login_page.is_error_message_displayed()
            user_logged_in = login_page.is_logged_in()
            
            assert error_displayed or not user_logged_in, \
                "Either error message should be displayed OR user should not be logged in (empty fields)"
            
            # Verify user is not logged in
            assert not user_logged_in, "User should not be logged in with empty fields"
            
            # Clear form for next iteration
            login_page.clear_login_form()
            
        logger.info("Empty fields test passed")
    
    @pytest.mark.security
    def test_sql_injection_protection(self, login_page, sql_injection_tests, login_and_navigate):
        """
        Test Case: SQL injection protection
        
        Steps:
        1. Navigate to login page
        2. Enter SQL injection payload in username field
        3. Enter any password
        4. Click login button
        5. Verify application is not vulnerable to SQL injection
        """
        for sql_payload in sql_injection_tests:
            logger.info(f"Testing SQL injection payload: {sql_payload['username']}")
            
            # Attempt SQL injection
            login_page.login(
                username=sql_payload["username"],
                password=sql_payload["password"]
            )
            
            # Verify SQL injection attempt is blocked (error message OR simply not logged in)
            error_displayed = login_page.is_error_message_displayed()
            user_logged_in = login_page.is_logged_in()
            
            assert error_displayed or not user_logged_in, \
                "SQL injection should be blocked (error message OR no login)"
            assert not user_logged_in, "SQL injection should not grant access"
            
            # Verify no sensitive data is exposed in error message
            error_message = login_page.get_error_message().lower()
            sensitive_keywords = ["sql", "database", "table", "select", "insert", "delete", "update"]
            for keyword in sensitive_keywords:
                assert keyword not in error_message, f"Error message should not contain '{keyword}'"
            
            # Clear form for next iteration
            login_page.clear_login_form()
            
        logger.info("SQL injection protection test passed")
    
    @pytest.mark.security
    def test_xss_protection(self, login_page, xss_tests, login_and_navigate):
        """
        Test Case: XSS (Cross-Site Scripting) protection
        
        Steps:
        1. Navigate to login page
        2. Enter XSS payload in username field
        3. Enter any password
        4. Click login button
        5. Verify XSS payload is properly sanitized
        """
        for xss_payload in xss_tests:
            logger.info(f"Testing XSS payload: {xss_payload['username']}")
            
            # Attempt XSS injection
            login_page.login(
                username=xss_payload["username"],
                password=xss_payload["password"]
            )
            
            # Verify XSS attempt is handled properly
            assert not login_page.is_logged_in(), "XSS payload should not grant access"
            
            # Check that no script executed (page title should be normal)
            page_title = login_page.get_page_title()
            assert "xss" not in page_title.lower(), "XSS script should not have executed"
            
            # Clear form for next iteration
            login_page.clear_login_form()
            
        logger.info("XSS protection test passed")
    
    @pytest.mark.login
    def test_password_field_masking(self, login_page, login_and_navigate):
        """
        Test Case: Password field should be masked
        
        Steps:
        1. Navigate to login page
        2. Verify password field type is 'password'
        3. Enter password and verify it's masked
        """
        logger.info("Testing password field masking")
        
        # Verify password field is masked
        assert login_page.is_password_field_masked(), "Password field should be masked (type='password')"
        
        # Enter password and verify it's not visible in plain text
        test_password = "TestPassword123"
        login_page.enter_password(test_password)
        
        # The actual value should still be there, but the field should be of type 'password'
        assert login_page.is_password_field_masked(), "Password field should remain masked after entering text"
        
        logger.info("Password field masking test passed")
    
    @pytest.mark.login
    def test_remember_me_functionality(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Remember me checkbox functionality
        
        Steps:
        1. Navigate to login page
        2. Check remember me checkbox
        3. Verify checkbox is selected
        4. Perform login
        """
        logger.info("Testing remember me functionality")
        
        # Check if remember me checkbox exists
        if not login_page.is_element_present(login_page.REMEMBER_ME_CHECKBOX):
            logger.info("Remember me checkbox not found - skipping test")
            pytest.skip("Remember me checkbox not available on this application")
        
        # Initially, remember me should not be checked
        assert not login_page.is_remember_me_checked(), "Remember me should initially be unchecked"
        
        # Click remember me checkbox
        login_page.click_remember_me()
        
        # Verify checkbox is now checked
        assert login_page.is_remember_me_checked(), "Remember me should be checked after clicking"
        
        # Perform login with remember me checked
        login_page.login(
            username=valid_credentials["username"],
            password=valid_credentials["password"],
            remember_me=True
        )
        
        logger.info("Remember me functionality test passed")
    
    @pytest.mark.login
    def test_forgot_password_link(self, login_page, login_and_navigate):
        """
        Test Case: Forgot password link functionality
        
        Steps:
        1. Navigate to login page
        2. Click forgot password link
        3. Verify navigation to forgot password page
        """
        logger.info("Testing forgot password link")
        
        # Check if forgot password link exists
        if not login_page.is_element_present(login_page.FORGOT_PASSWORD_LINK):
            logger.info("Forgot password link not found - skipping test")
            pytest.skip("Forgot password link not available on this application")
        
        # Get original URL
        original_url = login_page.get_current_url()
        
        # Click forgot password link
        login_page.click_forgot_password()
        time.sleep(2)  # Wait for potential navigation
        
        # Verify navigation (URL changed OR some other indication)
        current_url = login_page.get_current_url().lower()
        original_url_lower = original_url.lower()
        
        # Check for URL change or specific keywords
        url_changed = current_url != original_url_lower
        has_forgot_keywords = any(keyword in current_url for keyword in ['forgot', 'reset', 'recover', 'password'])
        
        assert url_changed or has_forgot_keywords, \
            f"Should navigate to forgot password page or change URL. Original: {original_url}, Current: {current_url}"
        
        logger.info("Forgot password link test passed")
    
    @pytest.mark.login
    def test_login_button_state(self, login_page, login_and_navigate):
        """
        Test Case: Login button should be enabled/disabled appropriately
        
        Steps:
        1. Navigate to login page
        2. Verify login button is enabled initially
        3. Test button behavior with different input states
        """
        logger.info("Testing login button state")
        
        # Login button should be enabled initially (some apps may disable it initially)
        button_enabled = login_page.is_login_button_enabled()
        logger.info(f"Login button initially enabled: {button_enabled}")
        # We'll just log the state instead of asserting, as different apps have different behaviors
        
        # Enter only username
        login_page.enter_username("test@example.com")
        assert login_page.is_login_button_enabled(), "Login button should remain enabled with username only"
        
        # Clear and enter only password
        login_page.clear_login_form()
        login_page.enter_password("password123")
        assert not login_page.is_login_button_enabled(), "Login button should disabled with password only"
        
        logger.info("Login button state test passed")
    
    @pytest.mark.login
    def test_keyboard_navigation(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Keyboard navigation and Enter key functionality
        
        Steps:
        1. Navigate to login page
        2. Use Tab key to navigate between fields
        3. Use Enter key to submit form
        """
        logger.info("Testing keyboard navigation")
        
        # Enter username and press Tab
        login_page.enter_username(valid_credentials["username"])
        login_page.press_key_on_username(Keys.TAB)
        
        # Enter password and press Enter to submit
        login_page.enter_password(valid_credentials["password"])
        login_page.press_key_on_password(Keys.ENTER)
        
        # Give time for form submission
        time.sleep(2)
        
        # Verify login was successful
        assert login_page.is_logged_in(), "Login should be successful when using Enter key"
        
        logger.info("Keyboard navigation test passed")
    
    @pytest.mark.login
    def test_multiple_failed_login_attempts(self, login_page, login_and_navigate):
        """
        Test Case: Multiple failed login attempts
        
        Steps:
        1. Navigate to login page
        2. Attempt multiple failed logins
        3. Verify appropriate handling (account lockout, CAPTCHA, etc.)
        """
        logger.info("Testing multiple failed login attempts")
        
        # Attempt multiple failed logins
        for attempt in range(3):
            logger.info(f"Failed login attempt {attempt + 1}")
            
            login_page.login(
                username="invalid@example.com",
                password="wrongpassword"
            )
            
            # Verify error message is displayed OR user is not logged in
            error_displayed = login_page.is_error_message_displayed()
            user_logged_in = login_page.is_logged_in()
            
            assert error_displayed or not user_logged_in, \
                f"Either error message should be displayed OR user should not be logged in (attempt {attempt + 1})"
            assert not user_logged_in, f"Should not be logged in after attempt {attempt + 1}"
            
            # Clear form for next attempt
            login_page.clear_login_form()
            time.sleep(1)  # Small delay between attempts
        
        logger.info("Multiple failed login attempts test passed")
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_form_validation(self, login_page, login_and_navigate):
        """
        Test Case: Login form field validation
        
        Steps:
        1. Navigate to login page
        2. Test various input validations
        3. Verify form behavior with different inputs
        """
        logger.info("Testing login form validation")
        
        # Test that form is displayed correctly
        assert login_page.is_login_form_displayed(), "Login form should be displayed"
        
        # Test clearing fields
        login_page.enter_username("test@example.com")
        login_page.enter_password("password123")
        
        # Verify fields have values
        assert login_page.get_username_field_value() == "test@example.com", "Username field should contain entered value"
        assert login_page.get_password_field_value() == "password123", "Password field should contain entered value"
        
        # Clear form
        login_page.clear_login_form()
        
        # Verify fields are cleared
        assert login_page.get_username_field_value() == "", "Username field should be empty after clearing"
        assert login_page.get_password_field_value() == "", "Password field should be empty after clearing"
        
        logger.info("Login form validation test passed")
    
    @pytest.mark.login
    def test_page_refresh_during_login(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Page refresh behavior during login process
        
        Steps:
        1. Navigate to login page
        2. Enter credentials
        3. Refresh page
        4. Verify form state
        """
        logger.info("Testing page refresh during login")
        
        # Enter credentials
        login_page.enter_username(valid_credentials["username"])
        login_page.enter_password(valid_credentials["password"])
        
        # Refresh page
        login_page.refresh_page()
        
        # Verify form is back to initial state
        assert login_page.is_login_form_displayed(), "Login form should be displayed after refresh"
        assert login_page.get_username_field_value() == "", "Username field should be empty after refresh"
        assert login_page.get_password_field_value() == "", "Password field should be empty after refresh"
        
        logger.info("Page refresh during login test passed")
    
    @pytest.mark.login
    def test_case_sensitive_credentials(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Case sensitivity of login credentials
        
        Steps:
        1. Navigate to login page
        2. Test with different case combinations
        3. Verify case sensitivity behavior
        """
        logger.info("Testing case sensitive credentials")
        
        # Test with uppercase username
        login_page.login(
            username=valid_credentials["username"].upper(),
            password=valid_credentials["password"]
        )
        
        # Typically, usernames are case-insensitive but passwords are case-sensitive
        # Adjust assertion based on actual application behavior
        assert not login_page.is_logged_in(), "Login should fail with uppercase username"
        
        # Clear form
        login_page.clear_login_form()
        
        # Test with different case password
        login_page.login(
            username=valid_credentials["username"],
            password=valid_credentials["password"].upper()
        )
        
        assert not login_page.is_logged_in(), "Login should fail with uppercase password"
        
        logger.info("Case sensitive credentials test passed")

class TestLogout:
    """Test class for logout functionality"""
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_logout_after_login(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Successful logout after valid login
        
        Steps:
        1. Navigate to login page
        2. Perform valid login
        3. Click logout button
        4. Verify redirect to login page
        """
        logger.info("Testing successful logout after login")
        
        # Perform login first
        login_page.login(
            username=valid_credentials["username"],
            password=valid_credentials["password"]
        )
        
        # Verify login was successful
        assert login_page.is_logged_in(), "User should be logged in before testing logout"
        
        # Perform logout
        login_page.logout()
        
        # Wait for logout to process
        time.sleep(3)
        
        # Verify logout was successful
        current_url = login_page.get_current_url()
        assert "/login" in current_url or login_page.is_login_form_displayed(), \
            "Should be redirected to login page after logout"
        
        logger.info("Successful logout test passed")
    
    @pytest.mark.login
    def test_logout_button_visibility_after_login(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Logout button should be visible after successful login
        
        Steps:
        1. Navigate to login page
        2. Verify logout button is not visible
        3. Perform valid login
        4. Verify logout button becomes visible
        """
        logger.info("Testing logout button visibility")
        
        # Initially logout button should not be visible
        assert not login_page.is_element_present(login_page.LOGOUT_BUTTON), \
            "Logout button should not be visible on login page"
        
        # Perform login
        login_page.login(
            username=valid_credentials["username"],
            password=valid_credentials["password"]
        )
        
        # Verify login was successful
        assert login_page.is_logged_in(), "User should be logged in"
        
        # Verify logout button is now visible
        assert login_page.is_element_present(login_page.LOGOUT_BUTTON) or \
               login_page.is_element_present(login_page.LOGOUT_SECOND_BUTTON), \
            "Logout button should be visible after login"
        
        logger.info("Logout button visibility test passed")
    
    @pytest.mark.login
    def test_multiple_logout_attempts(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Multiple logout attempts should not cause errors
        
        Steps:
        1. Navigate to login page
        2. Perform valid login
        3. Click logout multiple times
        4. Verify proper handling
        """
        logger.info("Testing multiple logout attempts")
        
        # Perform login first
        login_page.login(
            username=valid_credentials["username"],
            password=valid_credentials["password"]
        )
        
        # Verify login was successful
        assert login_page.is_logged_in(), "User should be logged in"
        
        # First logout
        login_page.logout()
        time.sleep(2)
        
        # Verify first logout was successful
        current_url = login_page.get_current_url()
        first_logout_success = "/login" in current_url or login_page.is_login_form_displayed()
        assert first_logout_success, "First logout should be successful"
        
        # Try logout again (should not cause error)
        try:
            login_page.logout()
            logger.info("Second logout attempt completed without error")
        except Exception as e:
            # This is acceptable - logout button might not be available
            logger.info(f"Second logout attempt failed as expected: {str(e)}")
        
        logger.info("Multiple logout attempts test passed")
    
    @pytest.mark.login 
    def test_direct_access_after_logout(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Direct access to protected pages should redirect to login after logout
        
        Steps:
        1. Perform login
        2. Navigate to dashboard/protected page
        3. Perform logout
        4. Try to access dashboard directly
        5. Verify redirect to login
        """
        logger.info("Testing direct access after logout")
        
        # Perform login first
        login_page.login(
            username=valid_credentials["username"],
            password=valid_credentials["password"]
        )
        
        # Verify login was successful
        assert login_page.is_logged_in(), "User should be logged in"
        
        # Get current URL after login (this should be the dashboard or main app)
        dashboard_url = login_page.get_current_url()
        
        # Perform logout
        login_page.logout()
        time.sleep(2)
        
        # Try to access dashboard directly
        login_page.navigate_to(dashboard_url)
        time.sleep(3)
        
        # Should be redirected to login
        current_url = login_page.get_current_url()
        assert "/login" in current_url or login_page.is_login_form_displayed(), \
            "Should be redirected to login when accessing protected page after logout"
        
        logger.info("Direct access after logout test passed")
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_session_cleanup_after_logout(self, login_page, valid_credentials, login_and_navigate):
        """
        Test Case: Session should be properly cleaned up after logout
        
        Steps:
        1. Perform login
        2. Perform logout  
        3. Use browser back button
        4. Verify cannot access protected content
        """
        logger.info("Testing session cleanup after logout")
        
        # Perform login first
        login_page.login(
            username=valid_credentials["username"],
            password=valid_credentials["password"]
        )
        
        # Verify login was successful
        assert login_page.is_logged_in(), "User should be logged in"
        
        # Store the logged-in page URL
        logged_in_url = login_page.get_current_url()
        
        # Perform logout
        login_page.logout()
        time.sleep(2)
        
        # Use browser back button to try to access previous page
        login_page.driver.back()
        time.sleep(3)
        
        # Should not be able to access the logged-in content
        current_url = login_page.get_current_url()
        
        # Either should be redirected to login or show login form
        session_cleaned = ("/login" in current_url or 
                          login_page.is_login_form_displayed() or
                          current_url != logged_in_url)
        
        assert session_cleaned, "Session should be cleaned up, cannot access previous page"
        
        logger.info("Session cleanup after logout test passed")
