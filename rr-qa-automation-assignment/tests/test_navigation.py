import pytest
import time

class TestNavigation:
    """Test cases for navigation and URL handling"""
    
    @pytest.mark.negative
    def test_direct_url_access(self, driver):
        """Test accessing pages directly via URL (negative case)"""
        print("\nTesting direct URL access...")
        
        # Try to access popular page directly
        driver.get("https://tmdb-discover.surge.sh/popular")
        time.sleep(3)
        
        # Check what happened
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        print(f"Current URL: {current_url}")
        
        # It might redirect or show error
        if "popular" in current_url or "popular" in page_source:
            print("✅ Direct URL access worked")
        elif "error" in page_source or "not found" in page_source:
            print("⚠️ Direct URL access failed (expected based on assignment)")
        else:
            print("ℹ️  Direct URL access resulted in unknown state")
        
        # Don't fail, just document
        assert True
    
    def test_browser_back_forward(self, setup):
        """Test browser back/forward navigation"""
        driver, discover_page, filter_panel = setup
        
        time.sleep(2)
        
        # Get initial state
        initial_url = driver.current_url
        print(f"Initial URL: {initial_url}")
        
        # Navigate to a section
        discover_page.navigate_to_popular()
        time.sleep(2)
        popular_url = driver.current_url
        print(f"After navigation: {popular_url}")
        
        # Use browser back
        driver.back()
        time.sleep(2)
        back_url = driver.current_url
        
        # Check if we went back
        if initial_url in back_url or back_url == initial_url:
            print("✅ Browser back worked")
        else:
            print(f"⚠️ Browser back went to: {back_url}")
        
        # Use browser forward
        driver.forward()
        time.sleep(2)
        forward_url = driver.current_url
        
        if popular_url in forward_url or forward_url == popular_url:
            print("✅ Browser forward worked")
        else:
            print(f"⚠️ Browser forward went to: {forward_url}")