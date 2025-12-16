# Amazon Deals - Multiple Data Sources

This project provides **three ways** to get Amazon deals data:

1. **Official PA API** (Best - when eligible)
2. **Web Scraper** (Alternative - may face bot detection)
3. **Sample Data Generator** (Immediate - for testing)

## Quick Start

### Option 1: Sample Data (Immediate) ✅

Generate sample deals data instantly for testing:

```bash
python generate_sample_deals.py
```

This creates `products.json` with realistic sample deals including your affiliate tag.

---

### Option 2: Official PA API (Recommended - Requires Eligibility)

Use Amazon's official Product Advertising API:

```bash
python fetch_amazon_deals.py
```

**Requirements:**
- Amazon Associate account with 3+ qualifying sales
- PA API access granted by Amazon

**Status:** Your account (`booksmanish-20`) needs to meet eligibility requirements.

---

### Option 3: Web Scraper (Alternative - May Face Challenges)

Scrape Amazon's Today's Deals page:

```bash
python scrape_amazon_deals.py
```

**Note:** Amazon has aggressive bot detection. This may not always work reliably.

---

## Files Overview

### Core Scripts

- **`fetch_amazon_deals.py`** - Official PA API integration (ready when eligible)
- **`scrape_amazon_deals.py`** - Web scraper using Selenium
- **`generate_sample_deals.py`** - Sample data generator (works immediately)

### Configuration

- **`config.py`** - PA API credentials and settings
- **`scraper_config.py`** - Web scraper settings
- **`scraper_utils.py`** - Utility functions for scraping

### Output

- **`products.json`** - Deals data in standardized JSON format

---

## Output Format

All three methods produce the same JSON structure:

```json
{
  "fetch_timestamp": "2025-12-16T17:19:22",
  "total_deals": 10,
  "source": "sample_data|web_scraper|pa_api",
  "products": [
    {
      "asin": "B09B8V1LZ3",
      "title": "Product Name",
      "current_price": "$22.99",
      "original_price": "$49.99",
      "savings": "USD 27.00",
      "savings_percentage": "54%",
      "currency": "USD",
      "is_prime_eligible": true,
      "promotions": [],
      "image_url": "https://...",
      "product_url": "https://www.amazon.com/dp/ASIN?tag=booksmanish-20"
    }
  ]
}
```

---

## Current Status

| Method | Status | Notes |
|--------|--------|-------|
| Sample Data | ✅ Working | Use for immediate testing |
| PA API | ⏳ Waiting | Need 3+ sales for eligibility |
| Web Scraper | ⚠️ Limited | May face bot detection |

---

## Recommendations

**For Development/Testing:**
- Use `generate_sample_deals.py` - works immediately

**For Production (Long-term):**
1. Generate 3+ sales through your affiliate links
2. Wait for PA API access
3. Use `fetch_amazon_deals.py` - most reliable and legal

**For Immediate Real Data:**
- Try `scrape_amazon_deals.py` but be aware of limitations
- Consider third-party APIs (Keepa, Rainforest API)

---

## Next Steps

1. **Now:** Use sample data generator for testing
2. **Soon:** Work on getting 3 sales for PA API access
3. **Future:** Switch to official PA API for production use

---

## Documentation

- **`README.md`** - This file
- **`API_ELIGIBILITY_SOLUTIONS.md`** - Detailed guide on PA API eligibility
- **Walkthrough** - Complete implementation documentation

---

## Support

All product URLs include your affiliate tag (`booksmanish-20`) so you can start earning commissions from any shared links!

For PA API eligibility questions, visit: https://affiliate-program.amazon.com/