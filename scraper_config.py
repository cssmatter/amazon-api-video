# Amazon Deals Scraper Configuration
import os

# Amazon URLs
# Amazon Best Sellers URLs
CATEGORIES = {
    "Best Sellers": "https://www.amazon.com/Best-Sellers/zgbs",
    "Movers & Shakers": "https://www.amazon.com/gp/movers-and-shakers",
    "New Releases": "https://www.amazon.com/gp/new-releases",
    "Books": "https://www.amazon.com/Best-Sellers-Books/zgbs/books",
    "Electronics": "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics",
    "Toys & Games": "https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games",
    "Kitchen": "https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen",
}

# Default target for backward compatibility (optional)
DEALS_URL = CATEGORIES["Best Sellers"]
BASE_URL = "https://www.amazon.com"

# Partner Tag for affiliate links
PARTNER_TAG = "booksmanish-20"

# Scraping Settings
MAX_DEALS = 20  # Maximum number of deals to scrape
SCROLL_PAUSE_TIME = 2  # Seconds to wait after scrolling
PAGE_LOAD_TIMEOUT = 30  # Seconds to wait for page load

# Browser Settings
HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'  # Run browser in headless mode (no GUI)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Rate Limiting
REQUEST_DELAY = 1  # Seconds to wait between requests (be respectful)

# Output
OUTPUT_FILE = "products.json"
