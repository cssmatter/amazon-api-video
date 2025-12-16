# Amazon Product Advertising API Configuration

# API Credentials
ACCESS_KEY = "AKPA98SSRM1765882731"
SECRET_KEY = "GC5Mm3eUEKcM9FizMVA0AurMZ0Fuwc59CP2mwj1p"

# IMPORTANT: You MUST provide your Amazon Associate Tag (Partner Tag)
# This is required for all PA API requests
# Get it from: https://affiliate-program.amazon.com/
PARTNER_TAG = "booksmanish-20"  # Amazon Associate Tag

# API Settings
REGION = "US"  # Country code: US, UK, IN, JP, etc.
HOST = "webservices.amazon.com"
MARKETPLACE = "www.amazon.com"

# Search Settings
SEARCH_KEYWORDS = "deals"  # Keywords to search for deals
SEARCH_INDEX = "All"  # Search across all categories
MAX_ITEMS = 10  # Maximum number of items to fetch

# Resources to request from API
RESOURCES = [
    "ItemInfo.Title",
    "ItemInfo.Features",
    "Offers.Listings.Price",
    "Offers.Listings.SavingBasis",
    "Offers.Listings.Promotions",
    "Offers.Listings.DeliveryInfo.IsPrimeEligible",
    "Images.Primary.Large",
]
