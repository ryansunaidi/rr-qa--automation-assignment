from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import re

class DiscoverPage(BasePage):
    # Navigation locators
    NAV_POPULAR = (By.XPATH, "//a[contains(@href, '/popular') or contains(text(), 'Popular')]")
    NAV_TREND = (By.XPATH, "//a[contains(@href, '/trend') or contains(text(), 'Trend')]")
    NAV_NEW = (By.XPATH, "//a[contains(@href, '/new') or contains(text(), 'New')]")
    NAV_TOP_RATED = (By.XPATH, "//a[contains(@href, '/top') or contains(text(), 'Top')]")
    
    # Movie cards locators
    MOVIE_CARDS = (By.XPATH, "//div[contains(@class, 'flex-col') and contains(@class, 'items-center')]")
    MOVIE_TITLES = (By.CSS_SELECTOR, "p.text-blue-500.font-bold.py-1")
    MOVIE_YEARS = (By.CSS_SELECTOR, "p.text-gray-500.font-light.text-sm")
    MOVIE_POSTERS = (By.CSS_SELECTOR, "img.w-60.h-96.object-contain")
    
    # Search locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='search']")
    SEARCH_ICON = (By.CSS_SELECTOR, "img[alt*='Search']")
    
    # Pagination locators
    PAGINATION_CONTAINER = (By.ID, "react-paginate")
    PAGINATION_NEXT = (By.CSS_SELECTOR, "li.next a")
    PAGINATION_PREV = (By.CSS_SELECTOR, "li.previous a")
    PAGINATION_PAGES = (By.CSS_SELECTOR, "#react-paginate li:not(.previous):not(.next) a")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_popular(self):
        try:
            self.click(self.NAV_POPULAR)
            self.logger.info("Navigated to Popular section")
        except Exception as e:
            self.logger.warning(f"Could not navigate to Popular: {e}")
    
    def navigate_to_trend(self):
        try:
            self.click(self.NAV_TREND)
            self.logger.info("Navigated to Trend section")
        except Exception as e:
            self.logger.warning(f"Could not navigate to Trend: {e}")
    
    def navigate_to_new(self):
        try:
            self.click(self.NAV_NEW)
            self.logger.info("Navigated to New section")
        except Exception as e:
            self.logger.warning(f"Could not navigate to New: {e}")
    
    def navigate_to_top_rated(self):
        try:
            self.click(self.NAV_TOP_RATED)
            self.logger.info("Navigated to Top Rated section")
        except Exception as e:
            self.logger.warning(f"Could not navigate to Top Rated: {e}")
    
    def search_movie(self, query):
        try:
            self.send_keys(self.SEARCH_INPUT, query)
            self.logger.info(f"Searched for: {query}")
        except Exception as e:
            self.logger.warning(f"Could not search: {e}")
    
    def get_movie_titles(self):
        try:
            titles = [title.text for title in self.find_elements(self.MOVIE_TITLES)]
            self.logger.info(f"Found {len(titles)} movie titles")
            return titles
        except:
            return []
    
    def get_movie_years(self):
        years = []
        try:
            year_elements = self.find_elements(self.MOVIE_YEARS)
            for element in year_elements:
                text = element.text
                # Extract year from text like "Horror, 2024" or "2024"
                year_match = re.search(r'\b(19|20)\d{2}\b', text)
                if year_match:
                    years.append(int(year_match.group()))
                elif text.strip().isdigit() and len(text.strip()) == 4:
                    # If the text is just a 4-digit year
                    year = int(text.strip())
                    if 1900 <= year <= 2100:
                        years.append(year)
        except Exception as e:
            self.logger.warning(f"Could not extract years: {e}")
        
        return years
    
    def get_movie_count(self):
        try:
            count = len(self.find_elements(self.MOVIE_CARDS))
            return count
        except:
            return 0
    
    def click_next_page(self):
        try:
            next_btn = self.find_element(self.PAGINATION_NEXT)
            # Check if button is disabled
            is_disabled = (
                "disabled" in next_btn.get_attribute("class") or 
                next_btn.get_attribute("aria-disabled") == "true" or
                "disabled" in self.driver.find_element(By.XPATH, "//li[contains(@class, 'next')]").get_attribute("class")
            )
            
            if not is_disabled:
                next_btn.click()
                self.logger.info("Clicked Next page")
                return True
            else:
                self.logger.info("Next button is disabled")
                return False
        except Exception as e:
            self.logger.warning(f"Could not click next page: {e}")
            return False
    
    def click_previous_page(self):
        try:
            prev_btn = self.find_element(self.PAGINATION_PREV)
            # Check if button is disabled
            is_disabled = (
                "disabled" in prev_btn.get_attribute("class") or 
                prev_btn.get_attribute("aria-disabled") == "true" or
                "disabled" in self.driver.find_element(By.XPATH, "//li[contains(@class, 'previous')]").get_attribute("class")
            )
            
            if not is_disabled:
                prev_btn.click()
                self.logger.info("Clicked Previous page")
                return True
            else:
                self.logger.info("Previous button is disabled")
                return False
        except Exception as e:
            self.logger.warning(f"Could not click previous page: {e}")
            return False
    
    def get_current_page_number(self):
        try:
            selected_page = self.driver.find_element(By.CSS_SELECTOR, "li.selected a")
            return int(selected_page.text)
        except:
            return 1
    
    def get_available_pages(self):
        """Get list of available page numbers"""
        pages = []
        try:
            page_elements = self.find_elements(self.PAGINATION_PAGES)
            for element in page_elements:
                text = element.text.strip()
                if text.isdigit():
                    pages.append(int(text))
        except:
            pass
        return pages