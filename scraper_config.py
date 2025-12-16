# Amazon Deals Scraper Configuration

# Amazon URLs
DEALS_URL = "https://www.amazon.com/gp/goldbox"  # Today's Deals page
BASE_URL = "https://www.amazon.com"

# Partner Tag for affiliate links
PARTNER_TAG = "booksmanish-20"

# Scraping Settings
MAX_DEALS = 20  # Maximum number of deals to scrape
SCROLL_PAUSE_TIME = 2  # Seconds to wait after scrolling
PAGE_LOAD_TIMEOUT = 30  # Seconds to wait for page load

# Browser Settings
HEADLESS = True  # Run browser in headless mode (no GUI)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Rate Limiting
REQUEST_DELAY = 1  # Seconds to wait between requests (be respectful)

# Output
OUTPUT_FILE = "products.json"
