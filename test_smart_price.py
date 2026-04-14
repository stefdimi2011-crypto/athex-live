import requests
from bs4 import BeautifulSoup
import re

url = "https://www.capital.gr/finance/quote/mtln/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"📥 Testing: {url}")
response = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the h1 with the stock name
h1 = soup.find('h1')
if h1:
    print(f"Stock: {h1.text}")
    
    # Get the parent section/div of h1
    parent = h1.parent
    print(f"\nLooking in parent element: {parent.name}")
    
    # Get text near h1 (next few elements after h1 in the same parent)
    all_text_in_parent = parent.get_text()
    print(f"Text in parent element:\n{all_text_in_parent[:300]}")
    
    # Find prices in this parent section
    prices = re.findall(r'(\d+[.,]\d+)', all_text_in_parent)
    print(f"\n\nPrices in stock header area: {prices[:10]}")
    
    # The main price is usually the first significant price after the symbol
    for price_str in prices[:5]:
        try:
            price_normalized = float(price_str.replace(',', '.'))
            if 0.1 < price_normalized < 100000:
                print(f"\n✅ Main price found: {price_str} = {price_normalized}")
                break
        except:
            pass
