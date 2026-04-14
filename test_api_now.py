import requests
import json

r = requests.get('http://127.0.0.1:5000/api/prices')
data = r.json()

print(f"Count: {data['count']}")
print(f"Last Update: {data['last_update']}")
if data['count'] > 0:
    sample = dict(list(data['prices'].items())[:5])
    print(f"Sample prices: {sample}")
    print("\n✅ SUCCESS - Prices are being returned!")
else:
    print("\n❌ FAILED - No prices returned")
