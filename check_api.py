import requests
import json

url = "https://www.capital.gr/api/quotes/MTLN"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    r = requests.get(url, headers=headers, timeout=5)
    if r.status_code == 200:
        data = r.json()
        if data.get('ResultData') and len(data['ResultData']) > 0:
            stock = data['ResultData'][0]
            print("=" * 60)
            print("Available fields in Capital.gr API:")
            print("=" * 60)
            for key in sorted(stock.keys()):
                print(f"{key:20} = {stock[key]}")
        else:
            print("No ResultData found")
    else:
        print(f"Error: {r.status_code}")
except Exception as e:
    print(f"Error: {e}")
