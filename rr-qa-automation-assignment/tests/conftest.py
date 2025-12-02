import pytest
import os
import stat
import tempfile
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config.config import Config
from utils.logger import Logger

def get_chromedriver_path():
    """Get ChromeDriver path, downloading if necessary"""
    
    # First check if we have a working chromedriver in PATH
    try:
        os.system("chromedriver --version 2>/dev/null")
        return "chromedriver"  # Use system chromedriver
    except:
        pass
    
    # Check in common locations
    common_paths = [
        "/usr/local/bin/chromedriver",
        "/opt/homebrew/bin/chromedriver",
        os.path.expanduser("~/chromedriver"),
        os.path.expanduser("~/.wdm/drivers/chromedriver/mac64/142.0.7444.175/chromedriver-mac-arm64/chromedriver")
    ]
    
    for path in common_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    
    # If not found, download it
    print("📥 ChromeDriver not found. Downloading...")
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    
    # Download ChromeDriver for Mac ARM
    chrome_version = "142.0.7444.175"
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/mac-arm64/chromedriver-mac-arm64.zip"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save and extract
        zip_path = os.path.join(temp_dir, "chromedriver.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Get chromedriver path
        chromedriver_path = os.path.join(temp_dir, "chromedriver-mac-arm64", "chromedriver")
        
        # Make executable
        os.chmod(chromedriver_path, stat.S_IEXEC)
        
        print(f"✅ ChromeDriver downloaded to: {chromedriver_path}")
        return chromedriver_path
        
    except Exception as e:
        print(f"❌ Failed to download ChromeDriver: {e}")
        
        # Fallback to Safari if on Mac
        if Config.IS_MAC_ARM:
            print("🔄 Trying Safari as fallback...")
            return "safari"
        raise

@pytest.fixture(scope="function")
def driver():
    """Fixture to create and tear down the WebDriver"""
    logger = Logger.get_logger()
    driver_instance = None
    
    try:
        # Get ChromeDriver path
        chromedriver_path = get_chromedriver_path()
        
        if chromedriver_path == "safari":
            # Use Safari on Mac
            driver_instance = webdriver.Safari()
            logger.info("Using Safari browser")
            
        else:
            # Use Chrome with custom options
            options = Options()
            
            if Config.HEADLESS:
                options.add_argument("--headless=new")  # New headless mode
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Add these to avoid detection
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Create service
            service = Service(executable_path=chromedriver_path)
            
            # Create driver
            driver_instance = webdriver.Chrome(service=service, options=options)
            
            # Stealth mode
            driver_instance.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
            })
            driver_instance.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info(f"ChromeDriver initialized from: {chromedriver_path}")
        
        # Set timeouts
        driver_instance.implicitly_wait(Config.IMPLICIT_WAIT)
        
        if Config.HEADLESS:
            driver_instance.set_window_size(1920, 1080)
        else:
            driver_instance.maximize_window()
        
        yield driver_instance
        
    except Exception as e:
        logger.error(f"Failed to initialize driver: {e}")
        
        # Last resort: try with system Chrome if available
        try:
            print("🔄 Trying system Chrome as last resort...")
            driver_instance = webdriver.Chrome()  # Let Selenium find it
            yield driver_instance
        except:
            raise
    
    finally:
        if driver_instance:
            driver_instance.quit()
            logger.info("Browser closed")

@pytest.fixture(scope="function")
def setup(driver):
    """Main setup fixture that provides driver and page objects"""
    logger = Logger.get_logger()
    
    # Navigate to base URL
    driver.get(Config.BASE_URL)
    logger.info(f"Navigated to {Config.BASE_URL}")
    
    # Import page objects here to avoid circular imports
    from pages.discover_page import DiscoverPage
    from pages.filter_panel import FilterPanel
    
    # Initialize page objects
    discover_page = DiscoverPage(driver)
    filter_panel = FilterPanel(driver)
    
    logger.info("Setup completed - page objects initialized")
    
    yield driver, discover_page, filter_panel
    
    logger.info("Test teardown completed")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to take screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver_fixture = item.funcargs.get('driver') or item.funcargs.get('setup')
        
        if driver_fixture:
            # Handle both cases: driver fixture directly or via setup fixture
            if isinstance(driver_fixture, tuple):
                # setup fixture returns (driver, discover_page, filter_panel)
                driver = driver_fixture[0]
            else:
                driver = driver_fixture
            
            if driver:
                test_name = item.name
                try:
                    # Take screenshot
                    screenshot_path = os.path.join(
                        Config.SCREENSHOT_DIR, 
                        f"FAIL_{test_name}_{Config.get_timestamp()}.png"
                    )
                    driver.save_screenshot(screenshot_path)
                    print(f"📸 Screenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"⚠️ Failed to save screenshot: {e}")