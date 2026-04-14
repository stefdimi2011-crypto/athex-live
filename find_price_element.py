import requests
from bs4 import BeautifulSoup
import re

url = "https://www.capital.gr/finance/quote/mtln/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

print("🔍 Looking for price element with detailed inspection...\n")

# Look for the main price (usually in a prominent element)
# Typical patterns for stock prices:
# 1. Large text near the top with the current price
# 2. Contains the stock symbol or "Price" label
# 3. Followed by % change

# Find all elements that might contain the price
candidates = []

# Look for elements with specific classes or data attributes related to price
for elem in soup.find_all(['span', 'div', 'p', 'strong', 'h2', 'h3']):
    classes = elem.get('class', [])
    data_attrs = {k: v for k, v in elem.attrs.items() if k.startswith('data-')}
    text = elem.text.strip()
    
    # Price typically is a number with comma (Greek format)
    if re.search(r'\d+[.,]\d+', text) and len(text) < 50:
        # Check if it's followed by % or change
        next_elem = elem.find_next(['span', 'div', 'p'])
        next_text = next_elem.text.strip() if next_elem else ""
        
        if '%' in next_text or 'MTLN' in elem.text or any(c in elem.get('class', []) for c in ['price', 'quote', 'current']):
            print(f"📊 Found candidate:")
            print(f"   Text: {text}")
            print(f"   Classes: {classes}")
            print(f"   Data attrs: {data_attrs}")
            print(f"   Next elem: {next_text[:50]}")
            print()

# Also look at the page title or main heading for hints
title = soup.find('h1')
if title:
    print(f"\n📌 Page title: {title.text}")

# Try to find the main content area
main = soup.find('main') or soup.find('div', class_='main') or soup.find('div', class_='container')
if main:
    # Look for the first few numbers with special formatting in the main area
    print("\n📍 Content from main area:")
    text_content = main.text[:500]
    prices = re.findall(r'\d+[.,]\d+', text_content)
    print(f"   Found prices: {prices[:5]}")
