import requests
from bs4 import BeautifulSoup
import re

# Get the stocks list page
url = "https://www.capital.gr/finance/allstocks"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print(f"📥 Λήψη {url}...")
response = requests.get(url, headers=headers, timeout=10)
print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')

print("\n🔍 Ψάχνω για links με stock codes...")
# Search for MTLN specifically
found_urls = set()
for link in soup.find_all('a', href=True):
    href = link['href']
    text = link.text.strip()
    
    # Look for MTLN or other stock codes
    if any(code in text or code in href for code in ['MTLN', 'ALPHA', 'OPAP', 'ATE ']):
        print(f"  Text: {text[:30]:30} | URL: {href}")
        found_urls.add(href)
    
    # Also capture any that look like stock symbols
    if re.match(r'^[A-Z]{3,6}$', text):
        if 'http' not in href:
            print(f"  SYMBOL: {text:10} | URL: {href}")
            found_urls.add(href)

# Look for any JSON data or data attributes that might have stock info
print("\n🔍 Ψάχνω για JSON data...")
if 'json' in response.text.lower():
    # Try to find JSON patterns
    json_patterns = re.findall(r'<script[^>]*type=[\'"]*application/json[\'"]*[^>]*>.*?</script>', response.text, re.DOTALL)
    if json_patterns:
        print(f"Found {len(json_patterns)} JSON blocks")
        print(json_patterns[0][:300])

print("\n📊 Summary of found URLs:")
for url in list(found_urls)[:10]:
    print(f"  {url}")
