import requests
import time

STOCKS_CONFIG = {
    "MTLN": "https://www.capital.gr/api/quotes/MTLN",
    "ETE": "https://www.capital.gr/api/quotes/ETE",
    "EUROB": "https://www.capital.gr/api/quotes/EUROB",
    "ALPHA": "https://www.capital.gr/api/quotes/ALPHA",
    "TPEIR": "https://www.capital.gr/api/quotes/TPEIR",
    "OPAP": "https://www.capital.gr/api/quotes/OPAP",
    "PPC": "https://www.capital.gr/api/quotes/PPC",
    "ADMIE": "https://www.capital.gr/api/quotes/ADMIE",
    "OTELE": "https://www.capital.gr/api/quotes/OTE",
    "TITK": "https://www.capital.gr/api/quotes/TITK",
    "LAMDA": "https://www.capital.gr/api/quotes/LAMDA",
    "HTO": "https://www.capital.gr/api/quotes/ELPE",
    "MYTIL": "https://www.capital.gr/api/quotes/MYTIL",
    "CENER": "https://www.capital.gr/api/quotes/CENER",
    "GEKTE": "https://www.capital.gr/api/quotes/GEK",
    "AEGN": "https://www.capital.gr/api/quotes/AEGE",
    "AVAX": "https://www.capital.gr/api/quotes/AVAX",
    "EXAE": "https://www.capital.gr/api/quotes/EXAE",
    "EYAPS": "https://www.capital.gr/api/quotes/EYDAP",
    "OLTH": "https://www.capital.gr/api/quotes/OLTH",
    "KRI": "https://www.capital.gr/api/quotes/KRI",
    "OLPIR": "https://www.capital.gr/api/quotes/OLP",
    "KARELIA": "https://www.capital.gr/api/quotes/KAREL",
    "INLOT": "https://www.capital.gr/api/quotes/INLO",
    "MODA": "https://www.capital.gr/api/quotes/MODA",
    "BYTE": "https://www.capital.gr/api/quotes/BYTE",
    "IASO": "https://www.capital.gr/api/quotes/IASO",
    "DOMIK": "https://www.capital.gr/api/quotes/DOMIK",
    "FLEXO": "https://www.capital.gr/api/quotes/FLEXO",
    "PPAK": "https://www.capital.gr/api/quotes/PPAK",
    "PETRO": "https://www.capital.gr/api/quotes/PETRO"
}

print("Testing all stocks...")
valid = []
invalid = []

for symbol, url in STOCKS_CONFIG.items():
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        data = response.json()
        
        if data.get('ResultData') and data['ResultData'][0] is not None:
            price = data['ResultData'][0].get('l')
            if price:
                valid.append((symbol, price))
                print(f"✅ {symbol}: {price}")
            else:
                invalid.append(symbol)
                print(f"❌ {symbol}: No price")
        else:
            invalid.append(symbol)
            print(f"❌ {symbol}: No data")
    except Exception as e:
        invalid.append(symbol)
        print(f"❌ {symbol}: {str(e)[:50]}")
    
    time.sleep(0.3)

print(f"\n\n📊 Summary:")
print(f"Valid: {len(valid)}/{len(STOCKS_CONFIG)}")
print(f"Invalid: {len(invalid)}")
print(f"\nValid symbols: {[v[0] for v in valid]}")
print(f"Invalid symbols: {invalid}")
