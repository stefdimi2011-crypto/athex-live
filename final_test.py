import requests
import json

r = requests.get('http://127.0.0.1:5000/api/prices')
data = r.json()
print(f"Status: {r.status_code}")
print(f"Count: {data['count']}")
print(f"Last Update: {data['last_update']}")
if data['count'] > 0:
    sample = dict(list(data['prices'].items())[:5])
    print(f"\nSample prices:")
    for sym, price in sample.items():
        print(f"  {sym}: {price}")
    print(f"\n✅ SUCCESS - All {data['count']} prices are being returned!")
else:
    print("\n❌ FAILED - No prices returned")
