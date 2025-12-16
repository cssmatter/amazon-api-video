"""
Amazon Deals Web Scraper - Utility Functions
Helper functions for scraping Amazon deals
"""

import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def setup_driver():
    """Initialize and configure Selenium WebDriver."""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import scraper_config
    
    options = Options()
    
    if scraper_config.HEADLESS:
        options.add_argument('--headless=new')
    
    options.add_argument(f'user-agent={scraper_config.USER_AGENT}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    # Disable automation flags
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver


def extract_asin(url):
    """
    Extract ASIN from Amazon product URL.
    
    Args:
        url: Amazon product URL
        
    Returns:
        str: ASIN or None if not found
    """
    if not url:
        return None
    
    # Pattern: /dp/ASIN or /gp/product/ASIN
    patterns = [
        r'/dp/([A-Z0-9]{10})',
        r'/gp/product/([A-Z0-9]{10})',
        r'/ASIN/([A-Z0-9]{10})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def parse_price(price_str):
    """
    Convert price string to float.
    
    Args:
        price_str: Price string like "$19.99" or "19.99"
        
    Returns:
        float: Price value or None if invalid
    """
    if not price_str:
        return None
    
    try:
        # Remove currency symbols and commas
        cleaned = re.sub(r'[^\d.]', '', price_str)
        return float(cleaned)
    except (ValueError, AttributeError):
        return None


def calculate_savings(original_price, current_price):
    """
    Calculate savings amount and percentage.
    
    Args:
        original_price: Original price (float)
        current_price: Current price (float)
        
    Returns:
        tuple: (savings_amount, savings_percentage) or (None, None)
    """
    if not original_price or not current_price:
        return None, None
    
    try:
        original = float(original_price)
        current = float(current_price)
        
        if original <= current:
            return None, None
        
        savings_amount = original - current
        savings_percentage = (savings_amount / original) * 100
        
        return savings_amount, savings_percentage
    except (ValueError, TypeError, ZeroDivisionError):
        return None, None


def add_affiliate_tag(url, partner_tag):
    """
    Append partner tag to product URL.
    
    Args:
        url: Product URL
        partner_tag: Amazon Associate tag
        
    Returns:
        str: URL with partner tag
    """
    if not url or not partner_tag:
        return url
    
    separator = '&' if '?' in url else '?'
    return f"{url}{separator}tag={partner_tag}"


def wait_for_element(driver, by, value, timeout=10):
    """
    Wait for element to be present on page.
    
    Args:
        driver: Selenium WebDriver
        by: Locator strategy (By.ID, By.CLASS_NAME, etc.)
        value: Locator value
        timeout: Maximum wait time in seconds
        
    Returns:
        WebElement or None if timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        return None


def scroll_page(driver, pause_time=2):
    """
    Scroll page to load lazy-loaded content.
    
    Args:
        driver: Selenium WebDriver
        pause_time: Time to wait after scrolling
    """
    # Get initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for page to load
        time.sleep(pause_time)
        
        # Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Break if no more content
        if new_height == last_height:
            break
        
        last_height = new_height


def safe_get_text(element, default=""):
    """
    Safely get text from element.
    
    Args:
        element: Selenium WebElement
        default: Default value if element is None
        
    Returns:
        str: Element text or default
    """
    try:
        return element.text.strip() if element else default
    except:
        return default


def safe_get_attribute(element, attribute, default=""):
    """
    Safely get attribute from element.
    
    Args:
        element: Selenium WebElement
        attribute: Attribute name
        default: Default value if element is None
        
    Returns:
        str: Attribute value or default
    """
    try:
        return element.get_attribute(attribute) if element else default
    except:
        return default
