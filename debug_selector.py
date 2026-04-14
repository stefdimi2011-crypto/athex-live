import requests
from bs4 import BeautifulSoup

url = "https://www.capital.gr/finance/quote/mtln/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(response.text, 'html.parser')

print("🔍 Finding all spans with 'price' in any class path:\n")

for span in soup.find_all(['span', 'div']):
    classes = span.get('class', [])
    text = span.text.strip()
    
    # Look for spans with 'price' in class
    if 'price' in str(classes).lower():
        print(f"Found element:")
        print(f"  Tag: {span.name}")
        print(f"  Classes: {classes}")
        print(f"  Text: {text[:50]}")
        print(f"  Attrs: {span.attrs}")
        print()

# Also try with lambda like in code
print("\n✅ Testing lambda selector (like in scrape_price):")
price_element = soup.find("span", {"class": lambda x: x and 'price' in x and 'bold' in x})
if price_element:
    print(f"Found: {price_element.text}")
else:
    print("Not found!")

# Try just 'price'
print("\n✅ Testing just 'price':")
price_element = soup.find("span", {"class": lambda x: x and 'price' in x})
if price_element:
    print(f"Found: {price_element.text}")
else:
    print("Not found!")

# Try bold
print("\n✅ Testing just 'bold':")
price_element = soup.find("span", {"class": lambda x: x and 'bold' in x})
if price_element:
    print(f"Found: {price_element.text}")
else:
    print("Not found!")
