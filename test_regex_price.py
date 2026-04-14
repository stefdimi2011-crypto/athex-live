import requests
from bs4 import BeautifulSoup
import re

url = "https://www.capital.gr/finance/quote/mtln/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"📥 Testing: {url}")
response = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(response.text, 'html.parser')

# Try regex method
print("\n🔍 Using regex to find price...")
text_content = soup.get_text()
prices = re.findall(r'(\d+[.,]\d+)', text_content)
print(f"Found {len(prices)} price patterns")

if prices:
    print(f"\nFirst 10 prices found: {prices[:10]}")
    
    for i, price_str in enumerate(prices[:20]):
        try:
            price_normalized = float(price_str.replace(',', '.'))
            if 0.1 < price_normalized < 100000:
                print(f"✅ Valid price #{i+1}: {price_str} (normalized: {price_normalized})")
                break
        except:
            pass
