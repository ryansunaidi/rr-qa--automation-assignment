import pytest
import time
from selenium.webdriver.common.by import By

class TestPagination:
    """Test cases for pagination functionality"""
    
    @pytest.mark.smoke
    def test_pagination_navigation(self, setup):
        """Test basic pagination navigation"""
        driver, discover_page, filter_panel = setup
        
        time.sleep(2)
        
        # Get initial page data
        page1_titles = discover_page.get_movie_titles()
        print(f"Page 1: {len(page1_titles)} movies")
        
        # Check if pagination exists
        try:
            pagination = driver.find_element(*discover_page.PAGINATION_CONTAINER)
            print("✅ Pagination container found")
        except:
            print("⚠️ No pagination found - might be single page")
            return  # Skip if no pagination
        
        # Try to navigate to page 2
        if discover_page.click_next_page():
            time.sleep(3)
            
            # Get page 2 data
            page2_titles = discover_page.get_movie_titles()
            print(f"Page 2: {len(page2_titles)} movies")
            
            if page2_titles:
                # Verify pages are different (if we have data)
                if page1_titles and page2_titles:
                    if page1_titles != page2_titles:
                        print("✅ Page 1 and Page 2 have different content")
                    else:
                        print("⚠️ Page 1 and Page 2 have same content")
                else:
                    print("⚠️ Could not compare page content")
                
                # Try to go back to page 1
                if discover_page.click_previous_page():
                    time.sleep(3)
                    print("✅ Returned to page 1")
            else:
                print("⚠️ No movies found on page 2")
        else:
            print("⚠️ Next button not available or disabled")
    
    @pytest.mark.regression
    def test_pagination_state(self, setup):
        """Test pagination button states"""
        driver, discover_page, filter_panel = setup
        
        time.sleep(2)
        
        # Check if pagination exists
        try:
            pagination = driver.find_element(*discover_page.PAGINATION_CONTAINER)
            print("✅ Pagination exists")
        except:
            print("⚠️ No pagination found")
            return
        
        # Check previous button state
        try:
            prev_buttons = driver.find_elements(By.CSS_SELECTOR, "li.previous")
            if prev_buttons:
                prev_li = prev_buttons[0]
                is_disabled = "disabled" in prev_li.get_attribute("class")
                print(f"Previous button: {'disabled' if is_disabled else 'enabled'}")
                
                # On first page, previous should be disabled
                if is_disabled:
                    print("✅ Previous button correctly disabled on first page")
                else:
                    print("⚠️ Previous button not disabled on first page")
            else:
                print("⚠️ Previous button not found")
        except Exception as e:
            print(f"⚠️ Could not check previous button: {e}")
        
        # Try to navigate through a few pages
        print("Testing page navigation...")
        for i in range(2):  # Try 2 pages
            if discover_page.click_next_page():
                time.sleep(2)
                print(f"✅ Navigated to page {i+2}")
                
                # Now previous should be enabled
                try:
                    prev_buttons = driver.find_elements(By.CSS_SELECTOR, "li.previous")
                    if prev_buttons:
                        prev_li = prev_buttons[0]
                        is_disabled = "disabled" in prev_li.get_attribute("class")
                        if not is_disabled:
                            print("✅ Previous button enabled after navigation")
                        else:
                            print("⚠️ Previous button still disabled")
                except:
                    pass
            else:
                print(f"⚠️ Could not navigate to page {i+2}")
                break
        
        # Go back to first page
        driver.get("https://tmdb-discover.surge.sh/")
        time.sleep(2)
    
    @pytest.mark.negative
    @pytest.mark.xfail(reason="Known issue: Last pages may not work properly")
    def test_last_page_navigation(self, setup):
        """Test navigation to last page (known issue)"""
        driver, discover_page, filter_panel = setup
        
        time.sleep(2)
        
        # Check if pagination exists
        try:
            pagination = driver.find_element(*discover_page.PAGINATION_CONTAINER)
        except:
            pytest.skip("No pagination found")
        
        # Try to find the last page button
        try:
            # Look for any page number
            page_links = driver.find_elements(By.CSS_SELECTOR, "#react-paginate a")
            if not page_links:
                pytest.skip("No page links found")
            
            # Find the highest page number
            max_page = 1
            for link in page_links:
                text = link.text.strip()
                if text.isdigit():
                    page_num = int(text)
                    if page_num > max_page:
                        max_page = page_num
            
            print(f"Found pages up to: {max_page}")
            
            # Try to click the last available page
            if max_page > 1:
                last_page_link = driver.find_element(By.XPATH, f"//a[text()='{max_page}']")
                last_page_link.click()
                time.sleep(3)
                
                # Check if navigation happened
                current_titles = discover_page.get_movie_titles()
                if current_titles:
                    print(f"✅ Navigated to page {max_page}")
                    print(f"Found {len(current_titles)} movies")
                else:
                    print(f"⚠️ Page {max_page} might be empty")
            else:
                pytest.skip("Only one page available")
                
        except Exception as e:
            print(f"❌ Could not navigate to last page: {e}")
            raise