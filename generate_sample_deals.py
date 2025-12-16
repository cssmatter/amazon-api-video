"""
Amazon Deals - Sample Data Generator
Creates sample deals data for testing without needing API access or web scraping
This is useful for development and testing while waiting for PA API eligibility
"""

import json
from datetime import datetime
import scraper_config


def generate_sample_deals(count=10):
    """
    Generate sample Amazon deals data.
    
    Args:
        count: Number of sample deals to generate
        
    Returns:
        list: List of sample deal dictionaries
    """
    sample_products = [
        {
            "title": "Echo Dot (5th Gen) Smart Speaker with Alexa",
            "asin": "B09B8V1LZ3",
            "current_price": "$22.99",
            "original_price": "$49.99",
            "discount_pct": 54
        },
        {
            "title": "Fire TV Stick 4K streaming device",
            "asin": "B0BP9SNVH9",
            "current_price": "$24.99",
            "original_price": "$49.99",
            "discount_pct": 50
        },
        {
            "title": "Kindle Paperwhite (16 GB) – Now with a 6.8\" display",
            "asin": "B08KTZ8249",
            "current_price": "$99.99",
            "original_price": "$149.99",
            "discount_pct": 33
        },
        {
            "title": "Apple AirPods Pro (2nd Generation)",
            "asin": "B0CHWRXH8B",
            "current_price": "$189.99",
            "original_price": "$249.00",
            "discount_pct": 24
        },
        {
            "title": "Samsung 65-Inch Class QLED 4K Q60C Series",
            "asin": "B0C1JT6SG9",
            "current_price": "$697.99",
            "original_price": "$1,099.99",
            "discount_pct": 37
        },
        {
            "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
            "asin": "B09XS7JWHH",
            "current_price": "$328.00",
            "original_price": "$399.99",
            "discount_pct": 18
        },
        {
            "title": "Instant Pot Duo 7-in-1 Electric Pressure Cooker",
            "asin": "B00FLYWNYQ",
            "current_price": "$79.00",
            "original_price": "$119.99",
            "discount_pct": 34
        },
        {
            "title": "Ninja AF101 Air Fryer, 4 Qt",
            "asin": "B07VH9HWC4",
            "current_price": "$69.99",
            "original_price": "$119.99",
            "discount_pct": 42
        },
        {
            "title": "Fitbit Charge 6 Fitness Tracker",
            "asin": "B0CC6DW6CT",
            "current_price": "$129.95",
            "original_price": "$159.95",
            "discount_pct": 19
        },
        {
            "title": "Bose QuietComfort Earbuds II",
            "asin": "B0B4PSKLZ4",
            "current_price": "$199.00",
            "original_price": "$299.00",
            "discount_pct": 33
        },
        {
            "title": "Dyson V8 Cordless Vacuum Cleaner",
            "asin": "B0B3YQNZ2K",
            "current_price": "$349.99",
            "original_price": "$469.99",
            "discount_pct": 26
        },
        {
            "title": "Keurig K-Mini Coffee Maker, Single Serve",
            "asin": "B07GV2S1GS",
            "current_price": "$59.99",
            "original_price": "$99.99",
            "discount_pct": 40
        },
        {
            "title": "Anker PowerCore 10000 Portable Charger",
            "asin": "B0194WDVHI",
            "current_price": "$19.99",
            "original_price": "$29.99",
            "discount_pct": 33
        },
        {
            "title": "Logitech MX Master 3S Wireless Mouse",
            "asin": "B09HM94VDS",
            "current_price": "$79.99",
            "original_price": "$99.99",
            "discount_pct": 20
        },
        {
            "title": "Philips Sonicare ProtectiveClean 4100 Electric Toothbrush",
            "asin": "B078GVMVRH",
            "current_price": "$29.96",
            "original_price": "$49.96",
            "discount_pct": 40
        }
    ]
    
    deals = []
    
    for i, product in enumerate(sample_products[:count]):
        # Calculate savings
        current_val = float(product["current_price"].replace('$', '').replace(',', ''))
        original_val = float(product["original_price"].replace('$', '').replace(',', ''))
        savings_amt = original_val - current_val
        
        deal = {
            "asin": product["asin"],
            "title": product["title"],
            "current_price": product["current_price"],
            "original_price": product["original_price"],
            "savings": f"USD {savings_amt:.2f}",
            "savings_percentage": f"{product['discount_pct']}%",
            "currency": "USD",
            "is_prime_eligible": i % 2 == 0,  # Alternate Prime eligibility
            "promotions": [],
            "image_url": f"https://m.media-amazon.com/images/I/placeholder-{product['asin']}.jpg",
            "product_url": f"https://www.amazon.com/dp/{product['asin']}?tag={scraper_config.PARTNER_TAG}"
        }
        
        deals.append(deal)
    
    return deals


def save_sample_deals(filename="products.json", count=10):
    """
    Generate and save sample deals to JSON file.
    
    Args:
        filename: Output filename
        count: Number of sample deals to generate
    """
    deals = generate_sample_deals(count)
    
    output = {
        "fetch_timestamp": datetime.now().isoformat(),
        "total_deals": len(deals),
        "source": "sample_data",
        "note": "Sample deals data for testing. Replace with real data from PA API or web scraper.",
        "products": deals
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(deals)} sample deals and saved to {filename}")
    return deals


def main():
    """Generate sample deals data."""
    print("=" * 60)
    print("Amazon Deals - Sample Data Generator")
    print("=" * 60)
    print("\nGenerating sample deals data...")
    print("This is for testing purposes while waiting for PA API access.\n")
    
    deals = save_sample_deals(count=10)
    
    print("\n" + "=" * 60)
    print("SAMPLE DEALS")
    print("=" * 60)
    
    for i, deal in enumerate(deals, 1):
        print(f"\n{i}. {deal['title']}")
        print(f"   ASIN: {deal['asin']}")
        print(f"   Price: {deal['current_price']} (was {deal['original_price']}) - Save {deal['savings_percentage']}")
        if deal['is_prime_eligible']:
            print(f"   [Prime] Prime Eligible")
    
    print("\n" + "=" * 60)
    print("Done! Sample data saved to products.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
