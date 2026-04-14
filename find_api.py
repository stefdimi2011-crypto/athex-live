import requests
import json

# Common API patterns for stock websites
api_patterns = [
    "https://www.capital.gr/api/quotes/MTLN",
    "https://www.capital.gr/api/quote/mtln",
    "https://www.capital.gr/api/price/mtln",
    "https://api.capital.gr/quotes/MTLN",
    "https://api.capital.gr/stocks/mtln",
    # Check if they have a JSON endpoint
    "https://www.capital.gr/quotes/MTLN?format=json",
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for url in api_patterns:
    try:
        print(f"\n🧪 Testing: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON Response found!")
                print(f"   Keys: {list(data.keys())[:10]}")
                break
            except:
                print(f"   Response is HTML (not JSON)")
                print(f"   Content length: {len(response.text)}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

# Also check if JS files in the page call an API
print("\n\n🔍 Checking for JavaScript API calls in capital.gr homepage...")
url = "https://www.capital.gr/"
response = requests.get(url, headers=headers, timeout=10)

# Look for fetch() or XHR calls
if '/api/' in response.text or 'fetch(' in response.text:
    print("Found API references in JS")
    # Find URLs mentioned
    import re
    api_urls = re.findall(r'["\'](/[\w/]+api[\w/]*)["\']', response.text)
    if api_urls:
        print(f"Potential API paths: {set(api_urls)}")
