import requests
import json

url = "https://www.capital.gr/api/quotes/MTLN"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"📥 Testing: {url}")
response = requests.get(url, headers=headers, timeout=10)
data = response.json()

print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])

# Get the price from ResultData
if data.get('ResultData'):
    result = data['ResultData']
    print("\n✅ ResultData keys:")
    if isinstance(result, dict):
        print(list(result.keys()))
    elif isinstance(result, list) and len(result) > 0:
        print(f"Array with {len(result)} items")
        print(list(result[0].keys()) if isinstance(result[0], dict) else "Not dict")
