"""
Amazon Product Advertising API - Fetch Latest Deals
This script fetches the latest deals from Amazon using the PA API 5.0
and stores them in a products.json file.
"""

import json
from datetime import datetime
from amazon.paapi import AmazonAPI

import config


def get_api_client():
    """Initialize and return the PA API client."""
    return AmazonAPI(
        access_key=config.ACCESS_KEY,
        secret_key=config.SECRET_KEY,
        partner_tag=config.PARTNER_TAG,
        country=config.REGION
    )


def search_deals(api_client):
    """
    Search for products with deals using the PA API.
    
    Args:
        api_client: The PA API client instance
        
    Returns:
        list: List of products with deal information
    """
    try:
        # Search for items
        items = api_client.search_items(
            keywords=config.SEARCH_KEYWORDS,
            item_count=config.MAX_ITEMS
        )
        
        if not items or not items.items:
            print("No search results found.")
            return []
        
        products = []
        
        # Process each item in the response
        for item in items.items:
            product = extract_product_info(item)
            if product:
                products.append(product)
        
        return products
        
    except Exception as e:
        print(f"Error calling PA API: {e}")
        return []


def extract_product_info(item):
    """
    Extract relevant product information from API response item.
    
    Args:
        item: AmazonProduct object from API response
        
    Returns:
        dict: Formatted product information
    """
    try:
        product = {
            "asin": None,
            "title": None,
            "current_price": None,
            "original_price": None,
            "savings": None,
            "savings_percentage": None,
            "currency": None,
            "is_prime_eligible": False,
            "promotions": [],
            "image_url": None,
            "product_url": None
        }
        
        # Extract ASIN
        if hasattr(item, 'asin'):
            product["asin"] = item.asin
        
        # Extract title
        if hasattr(item, 'item_info') and item.item_info:
            if hasattr(item.item_info, 'title') and item.item_info.title:
                product["title"] = item.item_info.title.display_value
        
        # Extract image
        if hasattr(item, 'images') and item.images:
            if hasattr(item.images, 'primary') and item.images.primary:
                if hasattr(item.images.primary, 'large') and item.images.primary.large:
                    product["image_url"] = item.images.primary.large.url
        
        # Extract product URL
        if hasattr(item, 'detail_page_url'):
            product["product_url"] = item.detail_page_url
        
        # Extract pricing and deal information
        if hasattr(item, 'offers') and item.offers:
            if hasattr(item.offers, 'listings') and item.offers.listings and len(item.offers.listings) > 0:
                listing = item.offers.listings[0]
                
                # Current price
                if hasattr(listing, 'price') and listing.price:
                    product["current_price"] = listing.price.display_amount
                    if hasattr(listing.price, 'currency'):
                        product["currency"] = listing.price.currency
                
                # Original price (savings basis)
                if hasattr(listing, 'saving_basis') and listing.saving_basis:
                    product["original_price"] = listing.saving_basis.display_amount
                    
                    # Calculate savings
                    if hasattr(listing, 'price') and listing.price and hasattr(listing.price, 'amount'):
                        try:
                            current = listing.price.amount
                            original = listing.saving_basis.amount
                            savings_amount = original - current
                            savings_pct = (savings_amount / original) * 100
                            
                            currency_symbol = product["currency"] if product["currency"] else "USD"
                            product["savings"] = f"{currency_symbol} {savings_amount:.2f}"
                            product["savings_percentage"] = f"{savings_pct:.0f}%"
                        except:
                            pass
                
                # Prime eligibility
                if hasattr(listing, 'delivery_info') and listing.delivery_info:
                    if hasattr(listing.delivery_info, 'is_prime_eligible'):
                        product["is_prime_eligible"] = listing.delivery_info.is_prime_eligible
                
                # Promotions
                if hasattr(listing, 'promotions') and listing.promotions:
                    for promo in listing.promotions:
                        promo_info = {}
                        if hasattr(promo, 'type'):
                            promo_info["type"] = promo.type
                        else:
                            promo_info["type"] = "Unknown"
                        
                        if hasattr(promo, 'discount_percent'):
                            promo_info["discount"] = f"{promo.discount_percent}%"
                        
                        if promo_info:
                            product["promotions"].append(promo_info)
        
        # Only return products that have some deal/savings information
        if product["savings"] or product["promotions"]:
            return product
        
        return None
        
    except Exception as e:
        print(f"Error extracting product info: {e}")
        return None


def save_to_json(products, filename="products.json"):
    """
    Save products to JSON file.
    
    Args:
        products: List of product dictionaries
        filename: Output filename
    """
    output = {
        "fetch_timestamp": datetime.now().isoformat(),
        "total_deals": len(products),
        "products": products
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully saved {len(products)} deals to {filename}")


def main():
    """Main function to fetch deals and save to JSON."""
    print("=" * 60)
    print("Amazon Product Advertising API - Deal Fetcher")
    print("=" * 60)
    
    # Validate configuration
    if config.PARTNER_TAG == "YOUR_ASSOCIATE_TAG_HERE":
        print("\n[!] ERROR: Partner Tag not configured!")
        print("Please update config.py with your Amazon Associate Tag.")
        print("Get your tag from: https://affiliate-program.amazon.com/")
        return
    
    print(f"\nSearching for: {config.SEARCH_KEYWORDS}")
    print(f"Marketplace: {config.MARKETPLACE}")
    print(f"Max items: {config.MAX_ITEMS}\n")
    
    # Initialize API client
    api_client = get_api_client()
    
    # Fetch deals
    print("Fetching deals from Amazon...")
    products = search_deals(api_client)
    
    if products:
        print(f"\nFound {len(products)} products with deals/savings!")
        
        # Save to JSON
        save_to_json(products)
        
        # Display summary
        print("\n" + "=" * 60)
        print("DEALS SUMMARY")
        print("=" * 60)
        for i, product in enumerate(products, 1):
            print(f"\n{i}. {product['title']}")
            print(f"   ASIN: {product['asin']}")
            if product['current_price']:
                print(f"   Price: {product['current_price']}", end="")
                if product['original_price']:
                    print(f" (was {product['original_price']})", end="")
                if product['savings_percentage']:
                    print(f" - Save {product['savings_percentage']}", end="")
                print()
            if product['is_prime_eligible']:
                print(f"   [Prime] Prime Eligible")
            if product['promotions']:
                for promo in product['promotions']:
                    print(f"   [Promo] {promo['type']}: {promo['discount']}")
    else:
        print("\nNo deals found. Try different search keywords or check your API credentials.")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
