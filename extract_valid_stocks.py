import requests
from bs4 import BeautifulSoup
import time

# Get the all stocks page and extract valid symbols
url = "https://www.capital.gr/finance/allstocks"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("Fetching valid stock list from capital.gr...")
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all stock symbols from the page
symbols = set()

# Look for links with finance/quote pattern
for link in soup.find_all('a', href=True):
    href = link['href']
    text = link.text.strip()
    
    if '/finance/quote/' in href:
        # Extract symbol from href or text
        if text and len(text) <= 8 and text.isupper():
            symbols.add(text)

print(f"\nFound {len(symbols)} valid symbols")
print("Valid symbols:", sorted(list(symbols))[:30])

# Now test a sample to verify they work
print("\n\nTesting a sample...")
test_symbols = list(sorted(symbols))[:10]

for symbol in test_symbols:
    url = f"https://www.capital.gr/api/quotes/{symbol}"
    try:
        response = requests.get(url, headers=headers, timeout=3)
        data = response.json()
        if data.get('ResultData') and data['ResultData'][0] is not None:
            price = data['ResultData'][0].get('l')
            print(f"✅ {symbol}: {price}")
        else:
            print(f"❌ {symbol}: No data in API")
    except:
        print(f"❌ {symbol}: Error")
    
    time.sleep(0.2)
