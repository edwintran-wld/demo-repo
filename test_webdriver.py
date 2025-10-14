"""
Simple WebDriver test to verify ChromeDriver is working correctly
"""

from utils.driver_factory import DriverFactory
import time

def test_webdriver():
    """Test if WebDriver can be created and used"""
    driver = None
    try:
        print("Creating ChromeDriver...")
        driver = DriverFactory.create_driver('chrome', headless=False)
        print("✅ ChromeDriver created successfully!")
        
        print("Testing navigation...")
        driver.get("https://www.google.com")
        time.sleep(2)
        
        print(f"✅ Navigation successful! Page title: {driver.title}")
        
        # Test SSL localhost navigation
        print("Testing SSL localhost navigation...")
        try:
            driver.get("https://localhost:4443/c/login")
            time.sleep(3)
            print(f"✅ SSL localhost navigation successful! Current URL: {driver.current_url}")
        except Exception as e:
            print(f"⚠️ SSL localhost navigation failed (this may be expected): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ WebDriver test failed: {e}")
        return False
        
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()

if __name__ == "__main__":
    success = test_webdriver()
    if success:
        print("\n🎉 WebDriver is working correctly!")
    else:
        print("\n❌ WebDriver test failed. Please check your Chrome installation.")
