import requests
from bs4 import BeautifulSoup
import re

# Get homepage and look for stock links
url = "https://www.capital.gr/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("📥 Λήψη homepage...")
response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

print("\n🔍 Ψάχνω για links με MTLN...")
# Search for links containing MTLN
for link in soup.find_all('a', href=True):
    href = link['href']
    if 'MTLN' in href or 'mtln' in href or 'stock' in href.lower():
        print(f"  Found: {href}")

print("\n🔍 Ψάχνω για patterns URLs...")
# Look for any stock-like patterns
for link in soup.find_all('a', href=True):
    href = link['href']
    # Look for Greek company patterns
    if any(x in href for x in ['quotes', 'stocks', 'shares', 'equities']):
        print(f"  Pattern: {href}")
        if 'ALPHA' in href or 'alpha' in href:
            print(f"    ^^^ Found Alpha: {href}")

print("\n📊 Sample of all href attributes (first 20 unique patterns):")
all_hrefs = list(set([link['href'] for link in soup.find_all('a', href=True)]))
for href in all_hrefs[:20]:
    print(f"  {href[:100]}")
