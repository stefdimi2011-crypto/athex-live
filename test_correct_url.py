import requests
from bs4 import BeautifulSoup

# Test the correct URL pattern
url = "https://www.capital.gr/finance/quote/mtln/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print(f"📥 Testing: {url}")
response = requests.get(url, headers=headers, timeout=10)
print(f"Status: {response.status_code}\n")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for price in various places
    print("🔍 Looking for price information...")
    
    # Try different selectors commonly used for stock prices
    price_patterns = [
        ('span.quote-price', 'span'),
        ('span.price', 'span'),
        ('div.price', 'div'),
        ('span[data-price]', 'span'),
        ('h1', 'h1'),
        ('h2', 'h2'),
    ]
    
    for pattern, tag in price_patterns:
        element = soup.find(tag, {"class": pattern.split('.')[-1]}) if '.' in pattern else soup.find(tag)
        if element:
            print(f"  Found in {tag}: {element.text.strip()[:100]}")
    
    # Look for all text containing digits and decimal points (likely price)
    print("\n📊 Text nodes that look like prices:")
    for elem in soup.find_all(['span', 'div', 'h1', 'h2']):
        text = elem.text.strip()
        # Look for patterns like "123,45" or "123.45"
        if len(text) < 20 and any(c.isdigit() for c in text):
            if ',' in text or '.' in text:
                print(f"  {text}")
else:
    print(f"❌ Failed to get page (status {response.status_code})")
