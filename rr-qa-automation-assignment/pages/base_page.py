from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import Config
from utils.logger import Logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = Logger.get_logger()
    
    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator):
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            return []
    
    def click(self, locator):
        element = self.find_element(locator)
        element.click()
        self.logger.info(f"Clicked on element: {locator}")
    
    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Entered text '{text}' in element: {locator}")
    
    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text
    
    def is_displayed(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False
    
    def take_screenshot(self, name):
        timestamp = Config.get_timestamp()
        filename = f"{Config.SCREENSHOT_DIR}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved: {filename}")
        return filename