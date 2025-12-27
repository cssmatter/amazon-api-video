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
        
        print(f"DEBUG: items type: {type(items)}")
        if isinstance(items, dict) and 'data' in items:
            products_list = items['data']
        elif isinstance(items, list):
            products_list = items
        else:
            print("Unknown response format from PA API.")
            return []
            
        products = []
        
        # Process each item in the response
        for item in products_list:
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
        item: AmazonProduct object or dictionary from API response
        
    Returns:
        dict: Formatted product information
    """
    try:
        # Helper to get value from either object attribute or dictionary key
        def get_val(obj, key, default=None):
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        product = {
            "asin": get_val(item, 'asin'),
            "title": None,
            "current_price": None,
            "original_price": None,
            "savings": None,
            "savings_percentage": None,
            "currency": None,
            "is_prime_eligible": False,
            "promotions": [],
            "image_url": None,
            "product_url": get_val(item, 'detail_page_url')
        }
        
        # Extract title
        item_info = get_val(item, 'item_info')
        if item_info:
            title_obj = get_val(item_info, 'title')
            if title_obj:
                product["title"] = get_val(title_obj, 'display_value')
        
        # Extract image
        images = get_val(item, 'images')
        if images:
            primary = get_val(images, 'primary')
            if primary:
                large = get_val(primary, 'large')
                if large:
                    product["image_url"] = get_val(large, 'url')
        
        # Extract pricing and deal information
        offers = get_val(item, 'offers')
        if offers:
            listings = get_val(offers, 'listings')
            if listings and len(listings) > 0:
                listing = listings[0]
                
                # Current price
                price = get_val(listing, 'price')
                if price:
                    product["current_price"] = get_val(price, 'display_amount')
                    product["currency"] = get_val(price, 'currency')
                
                # Original price (savings basis)
                saving_basis = get_val(listing, 'saving_basis')
                if saving_basis:
                    product["original_price"] = get_val(saving_basis, 'display_amount')
                    
                    # Calculate savings
                    if price:
                        price_amount = get_val(price, 'amount')
                        basis_amount = get_val(saving_basis, 'amount')
                        if price_amount is not None and basis_amount is not None:
                            try:
                                savings_amount = basis_amount - price_amount
                                if basis_amount > 0:
                                    savings_pct = (savings_amount / basis_amount) * 100
                                    currency_symbol = product["currency"] if product["currency"] else "USD"
                                    product["savings"] = f"{currency_symbol} {savings_amount:.2f}"
                                    product["savings_percentage"] = f"{savings_pct:.0f}%"
                            except:
                                pass
                
                # Prime eligibility
                delivery_info = get_val(listing, 'delivery_info')
                if delivery_info:
                    product["is_prime_eligible"] = get_val(delivery_info, 'is_prime_eligible', False)
                
                # Promotions
                promotions = get_val(listing, 'promotions')
                if promotions:
                    for promo in promotions:
                        promo_info = {
                            "type": get_val(promo, 'type', "Unknown"),
                            "discount": f"{get_val(promo, 'discount_percent')}%" if get_val(promo, 'discount_percent') else None
                        }
                        if promo_info["type"]:
                            product["promotions"].append(promo_info)
        
        # Return product even if no savings, since we want books, toys etc as well
        # But filter out those without a title or ASIN
        if product["asin"] and product["title"]:
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


import sys

def main():
    """Main function to fetch deals and save to JSON."""
    print("=" * 60)
    print("Amazon Product Advertising API - Deal Fetcher")
    print("=" * 60)
    
    # Check for keywords in command line arguments
    keywords = config.SEARCH_KEYWORDS
    if len(sys.argv) > 1:
        keywords = " ".join(sys.argv[1:])
        print(f"Using search keywords from command line: {keywords}")
    else:
        print(f"\nSearching for default keywords: {keywords}")

    # Validate configuration
    if config.PARTNER_TAG == "YOUR_ASSOCIATE_TAG_HERE":
        print("\n[!] ERROR: Partner Tag not configured!")
        print("Please update config.py with your Amazon Associate Tag.")
        print("Get your tag from: https://affiliate-program.amazon.com/")
        return
    
    print(f"Marketplace: {config.MARKETPLACE}")
    print(f"Max items: {config.MAX_ITEMS}\n")
    
    # Initialize API client
    api_client = get_api_client()
    
    # Fetch deals
    print(f"Fetching '{keywords}' from Amazon...")
    
    # Process products
    products = []
    try:
        # Search for items
        items = api_client.search_items(
            keywords=keywords,
            item_count=config.MAX_ITEMS
        )
        
        if isinstance(items, dict) and 'data' in items:
            products_list = items['data']
        elif isinstance(items, list):
            products_list = items
        else:
            print("Unknown response format from PA API.")
            return
            
        # Process each item
        for item in products_list:
            product = extract_product_info(item)
            if product:
                products.append(product)
                
    except Exception as e:
        print(f"Error calling PA API: {e}")
    
    if products:
        print(f"\nFound {len(products)} products!")
        
        # Save to JSON
        save_to_json(products)
        
        # Display summary
        print("\n" + "=" * 60)
        print("PRODUCTS SUMMARY")
        print("=" * 60)
        for i, product in enumerate(products, 1):
            print(f"\n{i}. {product['title']}")
            print(f"   ASIN: {product['asin']}")
            if product['current_price']:
                print(f"   Price: {product['current_price']}")
    else:
        print("\nNo products found. Try different search keywords.")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
