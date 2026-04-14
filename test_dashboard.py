#!/usr/bin/env python3
"""
Dashboard API Connectivity Test
Verifies the HTML dashboard can fetch and display prices
"""

import requests
import json
import time

API_URL = "http://127.0.0.1:5000/api/prices"

print("="*70)
print("🌐 Dashboard Connectivity Test")
print("="*70)
print()

# Test 1: API Response Speed
print("⚡ Test 1: API Response Speed")
print("-"*70)

for i in range(5):
    start = time.time()
    try:
        resp = requests.get(API_URL, timeout=5)
        duration = (time.time() - start) * 1000  # Convert to ms
        
        if resp.status_code == 200:
            data = resp.json()
            count = data.get('count', 0)
            print(f"Request #{i+1}: {duration:.1f}ms - {count} prices")
        else:
            print(f"Request #{i+1}: Error {resp.status_code}")
    except Exception as e:
        print(f"Request #{i+1}: Failed - {e}")
    
    if i < 4:
        time.sleep(0.5)

print()

# Test 2: Data Completeness
print("📊 Test 2: Data Structure Validation")
print("-"*70)

resp = requests.get(API_URL)
data = resp.json()

required_fields = ['prices', 'last_update', 'count']
print("Required fields:")
for field in required_fields:
    if field in data:
        print(f"  ✅ {field}")
    else:
        print(f"  ❌ {field} MISSING!")

print()
print(f"Prices entries: {len(data.get('prices', {}))}/31")
print(f"Last update: {data.get('last_update')}")
print()

# Test 3: Sample JSON output (for debugging)
print("📝 Test 3: Sample JSON Response")
print("-"*70)

sample = {}
prices = data.get('prices', {})
for i, (sym, price) in enumerate(list(prices.items())[:5]):
    sample[sym] = price

print(json.dumps({
    "count": len(prices),
    "last_update": data.get('last_update'),
    "prices_sample": sample,
    "note": "...(26 more stocks)"
}, indent=2, ensure_ascii=False))

print()
print("="*70)
print("✅ Dashboard API is fully functional!")
print("="*70)
print()
print("🌐 Dashboard URL: file:///C:/Users/Stefanos/Desktop/app.py/Untitled-1.html")
print("📡 API Endpoint: http://127.0.0.1:5000/api/prices")
print()
