"""
Helper utilities for test automation
"""
import json
import time
import random
from datetime import datetime
from config.config import Config

def wait_for_page_load(driver, timeout=10):
    """Wait for page to fully load"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        state = driver.execute_script("return document.readyState")
        if state == "complete":
            return True
        time.sleep(0.5)
    return False

def generate_test_data():
    """Generate test data for different test scenarios"""
    test_data = {
        "search_terms": ["Laberinto", "Kryptic", "Planet", "Drama", "2024"],
        "years": {
            "valid": [(2020, 2024), (2000, 2010), (1980, 1990)],
            "invalid": [(2025, 2020), (3000, 4000), (-1, 0)]
        },
        "ratings": [1, 3, 5]
    }
    return test_data

def take_full_page_screenshot(driver, name):
    """Take screenshot of entire page"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{Config.SCREENSHOT_DIR}/full_{name}_{timestamp}.png"
    
    # Store original size
    original_size = driver.get_window_size()
    
    # Get total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    # Set window size to capture full page
    driver.set_window_size(1920, total_height)
    
    # Take screenshot
    driver.save_screenshot(filename)
    
    # Restore original size
    driver.set_window_size(original_size['width'], original_size['height'])
    
    return filename

def extract_movie_info(element):
    """Extract movie information from a movie card element"""
    try:
        title = element.find_element_by_css_selector("p.text-blue-500.font-bold.py-1").text
        details = element.find_element_by_css_selector("p.text-gray-500.font-light.text-sm").text
        
        # Parse details for genre and year
        genre = ""
        year = None
        if "," in details:
            parts = details.split(",")
            if len(parts) >= 2:
                genre = parts[0].strip()
                year_text = parts[1].strip()
                # Extract year
                import re
                year_match = re.search(r'\b(19|20)\d{2}\b', year_text)
                if year_match:
                    year = int(year_match.group())
        
        return {
            "title": title,
            "genre": genre,
            "year": year,
            "details": details
        }
    except:
        return None