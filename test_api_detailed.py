import requests
import json
import time

test_stocks = ["MTLN", "CENER", "ALPHA"]

for symbol in test_stocks:
    url = f"https://www.capital.gr/api/quotes/{symbol}"
    print(f"Trying {symbol}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type')}")
        print(f"  Response length: {len(response.text)}")
        
        if response.text:
            data = response.json()
            print(f"  ✅ JSON parsed")
            print(f"  Keys: {list(data.keys())}")
            print(f"  ResultData: {data.get('ResultData')}")
        else:
            print(f"  ❌ Empty response")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    time.sleep(2)  # Add delay between requests
