"""
Amazon Deals Web Scraper
Scrapes Amazon's Today's Deals page and saves deals to products.json
Alternative to PA API while waiting for account eligibility
"""

import json
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import scraper_config
import scraper_utils


def scrape_deals():
    """
    Scrape deals from Amazon's Today's Deals page.
    
    Returns:
        list: List of deal dictionaries
    """
    print("Initializing browser...")
    driver = scraper_utils.setup_driver()
    deals = []
    
    try:
        print(f"Navigating to Amazon Deals page...")
        driver.get(scraper_config.DEALS_URL)
        
        # Wait for page to load
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Save page source for debugging
        print("Page loaded. Analyzing structure...")
        
        # Try multiple selectors for deal containers
        selectors = [
            "[data-testid='grid-deals-container'] > div",
            "div[data-deal-id]",
            ".DealCard-module__card",
            "div[class*='DealCard']",
            "div[class*='deal-card']",
            ".a-section.octopus-dlp-asin-section",
            "div.a-section[data-asin]"
        ]
        
        deal_elements = []
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"  Found {len(elements)} elements with selector: {selector}")
                    deal_elements = elements
                    break
            except:
                continue
        
        if not deal_elements:
            print("  No deal elements found with standard selectors.")
            print("  Trying to find all product links...")
            
            # Fallback: find all product links
            product_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/dp/']")
            print(f"  Found {len(product_links)} product links")
            
            if product_links:
                # Process product links directly
                count = 0
                for link in product_links[:scraper_config.MAX_DEALS]:
                    try:
                        deal = extract_deal_from_link(link, driver)
                        if deal:
                            deals.append(deal)
                            count += 1
                            print(f"  [{count}] {deal['title'][:50]}...")
                        
                        time.sleep(scraper_config.REQUEST_DELAY)
                    except Exception as e:
                        continue
        else:
            print(f"\nExtracting deal information from {len(deal_elements)} elements...")
            
            count = 0
            for deal_elem in deal_elements:
                if count >= scraper_config.MAX_DEALS:
                    break
                
                try:
                    deal = extract_deal_info(deal_elem, driver)
                    if deal:
                        deals.append(deal)
                        count += 1
                        print(f"  [{count}] {deal['title'][:50]}...")
                    
                    # Rate limiting
                    time.sleep(scraper_config.REQUEST_DELAY)
                    
                except Exception as e:
                    continue
        
        print(f"\nSuccessfully scraped {len(deals)} deals!")
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("Closing browser...")
        driver.quit()
    
    return deals


def extract_deal_from_link(link_elem, driver):
    """
    Extract deal information from a product link element (fallback method).
    
    Args:
        link_elem: Selenium WebElement for product link
        driver: Selenium WebDriver
        
    Returns:
        dict: Deal information or None if invalid
    """
    try:
        deal = {
            "asin": None,
            "title": None,
            "current_price": None,
            "original_price": None,
            "savings": None,
            "savings_percentage": None,
            "currency": "USD",
            "is_prime_eligible": False,
            "promotions": [],
            "image_url": None,
            "product_url": None
        }
        
        # Get product URL and ASIN
        product_url = link_elem.get_attribute("href")
        if not product_url:
            return None
        
        base_url = product_url.split('?')[0]
        deal["product_url"] = scraper_utils.add_affiliate_tag(base_url, scraper_config.PARTNER_TAG)
        deal["asin"] = scraper_utils.extract_asin(product_url)
        
        # Try to get title from link text or nearby elements
        title_text = scraper_utils.safe_get_text(link_elem)
        if not title_text or len(title_text) < 5:
            # Try to find title in parent or sibling elements
            try:
                parent = link_elem.find_element(By.XPATH, "..")
                title_text = scraper_utils.safe_get_text(parent)
            except:
                pass
        
        deal["title"] = title_text if title_text and len(title_text) > 5 else f"Product {deal['asin']}"
        
        # Try to find price near the link
        try:
            parent = link_elem.find_element(By.XPATH, "../..")
            price_elems = parent.find_elements(By.CSS_SELECTOR, "span[class*='price'], span.a-price-whole")
            if price_elems:
                deal["current_price"] = scraper_utils.safe_get_text(price_elems[0])
        except:
            pass
        
        # Only return if we have basic info
        if deal["asin"] and deal["title"]:
            return deal
        
        return None
        
    except Exception as e:
        return None


def extract_deal_info(deal_elem, driver):
    """
    Extract deal information from a deal element.
    
    Args:
        deal_elem: Selenium WebElement for deal card
        driver: Selenium WebDriver
        
    Returns:
        dict: Deal information or None if invalid
    """
    try:
        deal = {
            "asin": None,
            "title": None,
            "current_price": None,
            "original_price": None,
            "savings": None,
            "savings_percentage": None,
            "currency": "USD",
            "is_prime_eligible": False,
            "promotions": [],
            "image_url": None,
            "product_url": None
        }
        
        # Extract product link and ASIN
        try:
            link_elem = deal_elem.find_element(By.CSS_SELECTOR, "a[href*='/dp/']")
            product_url = link_elem.get_attribute("href")
            
            if product_url:
                # Clean URL (remove tracking parameters except our tag)
                base_url = product_url.split('?')[0]
                deal["product_url"] = scraper_utils.add_affiliate_tag(base_url, scraper_config.PARTNER_TAG)
                deal["asin"] = scraper_utils.extract_asin(product_url)
        except NoSuchElementException:
            return None
        
        # Extract title
        try:
            title_elem = deal_elem.find_element(By.CSS_SELECTOR, "[data-testid='deal-title']")
            deal["title"] = scraper_utils.safe_get_text(title_elem)
        except NoSuchElementException:
            # Try alternative selector
            try:
                title_elem = deal_elem.find_element(By.CSS_SELECTOR, "span[class*='title']")
                deal["title"] = scraper_utils.safe_get_text(title_elem)
            except:
                pass
        
        # Extract image
        try:
            img_elem = deal_elem.find_element(By.CSS_SELECTOR, "img")
            deal["image_url"] = scraper_utils.safe_get_attribute(img_elem, "src")
        except NoSuchElementException:
            pass
        
        # Extract current price
        try:
            price_elem = deal_elem.find_element(By.CSS_SELECTOR, "[data-testid='deal-price']")
            price_text = scraper_utils.safe_get_text(price_elem)
            deal["current_price"] = price_text
        except NoSuchElementException:
            # Try alternative selectors
            try:
                price_elem = deal_elem.find_element(By.CSS_SELECTOR, "span[class*='price']")
                price_text = scraper_utils.safe_get_text(price_elem)
                deal["current_price"] = price_text
            except:
                pass
        
        # Extract discount percentage
        try:
            discount_elem = deal_elem.find_element(By.CSS_SELECTOR, "[data-testid='deal-badge-price']")
            discount_text = scraper_utils.safe_get_text(discount_elem)
            
            if discount_text and '%' in discount_text:
                deal["savings_percentage"] = discount_text.strip()
                
                # Calculate original price if we have current price and percentage
                if deal["current_price"]:
                    current_val = scraper_utils.parse_price(deal["current_price"])
                    discount_pct = scraper_utils.parse_price(discount_text.replace('%', ''))
                    
                    if current_val and discount_pct:
                        original_val = current_val / (1 - discount_pct / 100)
                        deal["original_price"] = f"${original_val:.2f}"
                        savings_amt = original_val - current_val
                        deal["savings"] = f"USD {savings_amt:.2f}"
        except NoSuchElementException:
            pass
        
        # Check for Prime badge
        try:
            prime_elem = deal_elem.find_element(By.CSS_SELECTOR, "[aria-label*='Prime']")
            if prime_elem:
                deal["is_prime_eligible"] = True
        except NoSuchElementException:
            pass
        
        # Only return deals with minimum required information
        if deal["title"] and deal["product_url"] and (deal["current_price"] or deal["savings_percentage"]):
            return deal
        
        return None
        
    except Exception as e:
        print(f"    Error in extract_deal_info: {e}")
        return None


def save_to_json(deals, filename=None):
    """
    Save deals to JSON file.
    
    Args:
        deals: List of deal dictionaries
        filename: Output filename (default from config)
    """
    if filename is None:
        filename = scraper_config.OUTPUT_FILE
    
    output = {
        "fetch_timestamp": datetime.now().isoformat(),
        "total_deals": len(deals),
        "source": "web_scraper",
        "note": "Scraped from Amazon's Today's Deals page",
        "products": deals
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully saved {len(deals)} deals to {filename}")


def display_summary(deals):
    """Display summary of scraped deals."""
    if not deals:
        print("\nNo deals found.")
        return
    
    print("\n" + "=" * 60)
    print("DEALS SUMMARY")
    print("=" * 60)
    
    for i, deal in enumerate(deals, 1):
        print(f"\n{i}. {deal['title']}")
        if deal['asin']:
            print(f"   ASIN: {deal['asin']}")
        if deal['current_price']:
            print(f"   Price: {deal['current_price']}", end="")
            if deal['original_price']:
                print(f" (was {deal['original_price']})", end="")
            if deal['savings_percentage']:
                print(f" - Save {deal['savings_percentage']}", end="")
            print()
        if deal['is_prime_eligible']:
            print(f"   [Prime] Prime Eligible")
    
    print("\n" + "=" * 60)


def main():
    """Main function to scrape deals and save to JSON."""
    print("=" * 60)
    print("Amazon Deals Web Scraper")
    print("=" * 60)
    print(f"\nTarget: {scraper_config.DEALS_URL}")
    print(f"Max deals: {scraper_config.MAX_DEALS}")
    print(f"Headless mode: {scraper_config.HEADLESS}")
    print()
    
    # Scrape deals
    deals = scrape_deals()
    
    if deals:
        # Save to JSON
        save_to_json(deals)
        
        # Display summary
        display_summary(deals)
    else:
        print("\nNo deals were scraped. This could be due to:")
        print("  - Amazon's page structure changed")
        print("  - Network issues")
        print("  - Bot detection (try running with HEADLESS=False)")
        print("  - Rate limiting")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
