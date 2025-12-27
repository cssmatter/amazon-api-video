import os

# Amazon Product Advertising API Configuration

# API Credentials - Using environment variables for security
ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY", "AKPA98SSRM1765882731")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY", "GC5Mm3eUEKcM9FizMVA0AurMZ0Fuwc59CP2mwj1p")

# IMPORTANT: You MUST provide your Amazon Associate Tag (Partner Tag)
# Get it from: https://affiliate-program.amazon.com/
PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG", "booksmanish-20")  # Amazon Associate Tag

# API Settings
REGION = "US"  # Country code: US, UK, IN, JP, etc.
HOST = "webservices.amazon.com"
MARKETPLACE = "www.amazon.com"

# Search Settings
SEARCH_KEYWORDS = "Popular Romance books today"  # Keywords to search for deals
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

# Book Categories for Random Search
BOOK_CATEGORIES = [
    "Arts & Photography",
    "Award Winners",
    "Biographies & Memoirs",
    "Books on CD",
    "Business & Money",
    "Calendars",
    "Children's Books",
    "Christian Books & Bibles",
    "Comics & Graphic Novels",
    "Comics & Manga",
    "Computers & Technology",
    "Cookbooks, Food & Wine",
    "Crafts, Hobbies & Home",
    "Design",
    "Editors' Picks",
    "Education & Teaching",
    "Engineering & Transportation",
    "Health, Fitness & Dieting",
    "History",
    "Humor & Entertainment",
    "Law",
    "Lesbian, Gay, Bisexual & Transgender Books",
    "LGBTQIA+",
    "Libros en español",
    "Literature & Fiction",
    "Medical Books",
    "Mystery, Thriller & Suspense",
    "New, Used & Rental Textbooks",
    "Parenting & Relationships",
    "Politics & Social Sciences",
    "Reference",
    "Religion & Spirituality",
    "Romance",
    "Science & Math",
    "Science Fiction & Fantasy",
    "Self-Help",
    "Sports & Outdoors",
    "Teacher's Picks",
    "Teens",
    "Teen & Young Adult",
    "Test Preparation",
    "Travel"
]
