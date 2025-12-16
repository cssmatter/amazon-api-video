# Amazon Product Advertising API - Deal Fetcher

This project integrates with Amazon's Product Advertising API (PA API) 5.0 to fetch the latest deals and store them in a `products.json` file.

## Prerequisites

1. **Amazon Associate Account**: You need an Amazon Associate account to get your Partner Tag (Associate Tag)
2. **PA API Credentials**: Access Key and Secret Key from Amazon PA API
3. **Python 3.7+**: Make sure Python is installed on your system

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

Edit `config.py` and update the following:

- **PARTNER_TAG**: Replace `"YOUR_ASSOCIATE_TAG_HERE"` with your actual Amazon Associate Tag
  - Get it from: https://affiliate-program.amazon.com/
- **ACCESS_KEY**: Already configured
- **SECRET_KEY**: Already configured

### 3. Optional Configuration

You can also customize these settings in `config.py`:

- **REGION**: Change marketplace region (default: `us-east-1` for US)
- **SEARCH_KEYWORDS**: Modify search terms to find specific deals (default: `"deals"`)
- **SEARCH_INDEX**: Change product category (default: `"All"`)
- **MAX_ITEMS**: Number of items to fetch (default: `10`)

## Usage

Run the script to fetch deals:

```bash
python fetch_amazon_deals.py
```

The script will:
1. Connect to Amazon PA API using your credentials
2. Search for products with deals/savings
3. Extract product information including prices, savings, and promotions
4. Save the results to `products.json`

## Output Format

The `products.json` file contains:

```json
{
  "fetch_timestamp": "2025-12-16T16:48:23+05:30",
  "total_deals": 5,
  "products": [
    {
      "asin": "B0XXXXXXXX",
      "title": "Product Name",
      "current_price": "$19.99",
      "original_price": "$29.99",
      "savings": "USD 10.00",
      "savings_percentage": "33%",
      "currency": "USD",
      "is_prime_eligible": true,
      "promotions": [],
      "image_url": "https://...",
      "product_url": "https://www.amazon.com/dp/B0XXXXXXXX?tag=..."
    }
  ]
}
```

## Features

- ✅ Fetches products with active deals and savings
- ✅ Extracts pricing information (current price, original price, savings)
- ✅ Identifies Prime-eligible products
- ✅ Captures product promotions
- ✅ Includes product images and URLs
- ✅ Comprehensive error handling
- ✅ Clean JSON output format

## Troubleshooting

### "Partner Tag not configured" Error

Make sure you've updated `config.py` with your actual Amazon Associate Tag.

### API Authentication Errors

Verify that your Access Key and Secret Key are correct in `config.py`.

### No Deals Found

Try different search keywords or increase `MAX_ITEMS` in `config.py`.

## API Resources

- [Amazon PA API Documentation](https://webservices.amazon.com/paapi5/documentation/)
- [Amazon Associates Program](https://affiliate-program.amazon.com/)
- [PA API Python SDK](https://github.com/amzn/paapi5-python-sdk)

## License

This project is for educational and personal use with Amazon's Product Advertising API.