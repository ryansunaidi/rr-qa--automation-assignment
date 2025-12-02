import os
import platform
from datetime import datetime

class Config:
    BASE_URL = "https://tmdb-discover.surge.sh/"
    
    # Detect if we're on ARM Mac
    IS_MAC_ARM = platform.system() == 'Darwin' and platform.machine() == 'arm64'
    
    # Use Chrome for ARM Mac, otherwise regular Chrome
    BROWSER = "chrome"
    
    HEADLESS = False  # Set to True if you don't want to see browser
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    SCREENSHOT_DIR = "screenshots"
    REPORT_DIR = "reports"
    
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y%m%d_%H%M%S")