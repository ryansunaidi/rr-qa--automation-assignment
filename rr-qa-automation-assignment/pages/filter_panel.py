from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FilterPanel(BasePage):
    # Type filter
    TYPE_DROPDOWN = (By.CSS_SELECTOR, "div[class*='css-yk16xz-control']")
    TYPE_OPTIONS = (By.CSS_SELECTOR, "div[class*='css-1uccc91-singleValue']")
    
    # Genre filter
    GENRE_DROPDOWN = (By.XPATH, "//p[contains(text(), 'Genre')]/following-sibling::div")
    
    # Year filter
    YEAR_FROM_CONTAINER = (By.XPATH, "//div[contains(text(), '1900') or contains(@class, 'css-1uccc91-singleValue')][1]")
    YEAR_TO_CONTAINER = (By.XPATH, "//div[contains(text(), '2024') or contains(@class, 'css-1uccc91-singleValue')][2]")
    
    # Rating filter
    RATING_STARS = (By.CLASS_NAME, "rc-rate-star")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def select_type(self, type_name="Movie"):
        try:
            self.click(self.TYPE_DROPDOWN)
            self.logger.info(f"Clicked type dropdown")
            # Note: The actual selection would require handling the dropdown
            # For now, we just log that we tried
        except Exception as e:
            self.logger.warning(f"Could not select type: {e}")
    
    def select_genre(self, genre_name):
        try:
            self.click(self.GENRE_DROPDOWN)
            self.logger.info(f"Clicked genre dropdown")
            # Note: The actual selection would require handling the dropdown
        except Exception as e:
            self.logger.warning(f"Could not select genre: {e}")
    
    def set_year_range(self, year_from, year_to):
        try:
            self.logger.info(f"Setting year range: {year_from} - {year_to}")
            # Note: The actual year setting would require handling dropdowns
            # For demo purposes, we just log it
        except Exception as e:
            self.logger.warning(f"Could not set year range: {e}")
    
    def set_rating(self, stars):
        try:
            rating_stars = self.find_elements(self.RATING_STARS)
            if 1 <= stars <= len(rating_stars):
                rating_stars[stars-1].click()
                self.logger.info(f"Set rating to {stars} stars")
        except Exception as e:
            self.logger.warning(f"Could not set rating: {e}")