import json
from datetime import datetime

def generate_blog(input_file="products.json", output_file="index.html"):
    """
    Generate a static HTML blog page from products.json data.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = data.get('products', [])
        fetch_timestamp = data.get('fetch_timestamp', '')
        formatted_date = datetime.fromisoformat(fetch_timestamp).strftime('%B %d, %Y - %I:%M %p') if fetch_timestamp else "Recently"
        
        # HTML Header
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon Deals Blog</title>
    <style>
        :root {{
            --primary-color: #232f3e;
            --accent-color: #febd69;
            --text-color: #111;
            --bg-color: #f3f3f3;
            --card-bg: #fff;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            background-color: var(--primary-color);
            color: white;
            padding: 40px 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            margin: 0;
            font-size: 2.5rem;
            color: var(--accent-color);
        }}
        .timestamp {{
            font-size: 0.9rem;
            opacity: 0.8;
            margin-top: 10px;
        }}
        .product-card {{
            background-color: var(--card-bg);
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }}
        .product-card:hover {{
            transform: translateY(-5px);
        }}
        .product-title {{
            font-size: 1.5rem;
            margin-top: 0;
            margin-bottom: 20px;
            color: var(--primary-color);
        }}
        .product-image {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto 20px;
            border-radius: 4px;
        }}
        .price-section {{
            margin: 20px 0;
            font-size: 1.2rem;
        }}
        .current-price {{
            font-weight: bold;
            color: #b12704;
            font-size: 1.5rem;
        }}
        .savings {{
            color: #565959;
            font-size: 0.9rem;
            margin-left: 10px;
        }}
        .btn-container {{
            text-align: center;
            margin-top: 30px;
        }}
        .view-offer-btn {{
            background-color: var(--accent-color);
            color: var(--text-color);
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            display: inline-block;
            transition: background-color 0.2s;
            border: 1px solid #a88734;
        }}
        .view-offer-btn:hover {{
            background-color: #f3a847;
        }}
        hr {{
            border: 0;
            height: 1px;
            background: #eee;
            margin: 40px 0;
        }}
        footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Today's Best Amazon Deals</h1>
            <div class="timestamp">Last updated: {formatted_date}</div>
        </div>
    </header>
    
    <div class="container">
"""
        
        # Products Loop
        for product in products:
            title = product.get('title', 'Amazon Product')
            image_url = product.get('image_url', '')
            product_url = product.get('product_url', '#')
            price = product.get('current_price', 'Price not available')
            savings = product.get('savings_percentage', '')
            
            savings_html = f'<span class="savings">({savings} OFF)</span>' if savings else ''
            
            html_content += f"""
        <article class="product-card">
            <h2 class="product-title">{title}</h2>
            <img src="{image_url}" alt="{title}" class="product-image">
            <div class="price-section">
                <span class="current-price">{price}</span>
                {savings_html}
            </div>
            <div class="btn-container">
                <a href="{product_url}" target="_blank" class="view-offer-btn">View Offer on Amazon</a>
            </div>
        </article>
"""

        # HTML Footer
        html_content += """
    </div>
    
    <footer>
        <div class="container">
            <p>&copy; 2025 Amazon Deals Blog. All rights reserved.</p>
            <p>As an Amazon Associate I earn from qualifying purchases.</p>
        </div>
    </footer>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Successfully generated blog at {output_file}")
        
    except Exception as e:
        print(f"Error generating blog: {e}")

if __name__ == "__main__":
    generate_blog()
