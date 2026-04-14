import requests
from bs4 import BeautifulSoup

# Test different URL patterns for MTLN (Mytilineos - μια από τις μεγάλες μετοχές)
urls_to_test = [
    "https://www.capital.gr/quotes/MTLN",  # Current (fails with 404)
    "https://www.capital.gr/stocks/MTLN",
    "https://www.capital.gr/equities/MTLN",
    "https://www.capital.gr/MTLN",
    "https://www.capital.gr/stocks/GR0123456789",  # ISIN format
    "https://www.capital.gr/",  # Homepage to see structure
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for url in urls_to_test:
    try:
        print(f"\n🧪 Testing: {url}")
        response = requests.get(url, headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS! Content length: {len(response.text)}")
            # Show a bit of the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            if title:
                print(f"   Title: {title.text[:80]}")
        else:
            print(f"   ❌ Failed")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")
