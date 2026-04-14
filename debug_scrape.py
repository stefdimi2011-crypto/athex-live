import requests
from bs4 import BeautifulSoup
import time

# Test one URL to see what's happening
url = "https://www.capital.gr/quotes/MTLN"
print(f"Testing: {url}\n")

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"⏳ Ζητώ τη σελίδα... ({time.time()})")
    response = requests.get(url, headers=headers, timeout=10)
    print(f"✅ Λήφθηκε: status={response.status_code}")
    
    print(f"\n📄 Τμήμα HTML (πρώτοι 500 χαρακτήρες):\n{response.text[:500]}\n")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ψάχνω για price elements
    print("🔍 Ψάχνω για στοιχεία τιμής...")
    
    # Δοκιμάστε διάφορα CSS classes
    price_candidates = [
        soup.find("span", {"class": "quote-price"}),
        soup.find("div", {"class": "price"}),
        soup.find("span", {"class": "price"}),
        soup.find("div", {"class": "quote-price"}),
    ]
    
    for i, candidate in enumerate(price_candidates):
        if candidate:
            print(f"✅ Βρέθηκε στην προσπάθεια {i+1}: {candidate.text.strip()}")
        else:
            print(f"❌ Δεν βρέθηκε στην προσπάθεια {i+1}")
    
    # Περισσότερες πληροφορίες
    print(f"\n📊 Όλα τα σπαν στη σελίδα:")
    spans = soup.find_all("span")
    for span in spans[:10]:
        print(f"  - {span.text.strip()[:50]}")
    
except Exception as e:
    print(f"❌ Σφάλμα: {e}")
