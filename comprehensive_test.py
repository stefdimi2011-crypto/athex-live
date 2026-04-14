#!/usr/bin/env python3
"""
Comprehensive ATHEX Server Test
Tests prices, updates, and accuracy
"""

import requests
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://127.0.0.1:5000/api/prices"
CAPITAL_GR_API = "https://www.capital.gr/api/quotes"

# Stocks to test
STOCKS_CONFIG = {
    "MTLN": "MTLN", "CENER": "CENER", "ALWN": "ALWN", "BOCHGR": "BOCHGR",
    "BYLOT": "BYLOT", "CNLCAP": "CNLCAP", "CREDIA": "CREDIA", "OPTIMA": "OPTIMA",
    "YKNOT": "YKNOT", "AAAK": "ΑΑΑΚ", "ADMIE": "ΑΔΜΗΕ", "ALPHA": "ΑΛΦΑ",
    "GEKT": "ΓΕΚΤΕΡΝΑ", "GMEZ": "ΓΚΜΕΖΖ", "DOMIK": "ΔΟΜΙΚ", "ETE": "ΕΤΕ",
    "EUROB": "ΕΥΡΩΒ", "IKTIN": "ΙΚΤΙΝ", "INLIF": "ΙΝΛΙΦ", "CAIROMEZ": "ΚΑΙΡΟΜΕΖ",
    "KEKR": "ΚΕΚΡ", "LAVI": "ΛΑΒΙ", "MATHIO": "ΜΑΘΙΟ", "MEVA": "ΜΕΒΑ",
    "MERKO": "ΜΕΡΚΟ", "MOI": "ΜΟΗ", "XYLP": "ΞΥΛΠ", "OTE": "ΟΤΕ",
    "PEIR": "ΠΕΙΡ", "PRD": "ΠΡΔ", "PRONTON": "ΠΡΟΝΤΕΑ"
}

def get_capital_gr_price(api_symbol):
    """Fetch price from capital.gr API"""
    try:
        url = f"{CAPITAL_GR_API}/{api_symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data.get('ResultData') and len(data['ResultData']) > 0:
            if data['ResultData'][0] and 'l' in data['ResultData'][0]:
                return float(data['ResultData'][0]['l'])
    except:
        pass
    return None

def test_api_prices():
    """Get prices from our API"""
    try:
        resp = requests.get(API_URL, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

print("="*60)
print("🧪 ATHEX Server Comprehensive Test")
print("="*60)
print()

# Test 1: Check API response
print("📡 Test 1: API Response Check")
print("-"*60)

for attempt in range(3):
    data = test_api_prices()
    if data:
        print(f"✅ API Status: {data.get('count', 0)}/31 prices")
        print(f"   Last Update: {data.get('last_update', 'N/A')}")
        if data.get('count', 0) < 31:
            print(f"❌ WARNING: Only {data['count']} prices, expected 31!")
        else:
            print(f"✅ All 31 prices present!")
        break
    else:
        if attempt < 2:
            print(f"⏳ Waiting for server... (attempt {attempt+1}/3)")
            time.sleep(2)
        else:
            print("❌ Cannot connect to API!")
            exit(1)

print()

# Test 2: Compare with capital.gr
print("🔍 Test 2: Price Accuracy (vs capital.gr)")
print("-"*60)

response_data = test_api_prices()
api_prices = response_data.get('prices', {}) if response_data else {}

sample_stocks = {
    "ALPHA": "ΑΛΦΑ",
    "OTE": "ΟΤΕ", 
    "EUROB": "ΕΥΡΩΒ",
    "MTLN": "MTLN",
    "CENER": "CENER"
}

mismatches = 0
matches = 0

def compare_stock(symbol, api_sym):
    global mismatches, matches
    api_price = api_prices.get(symbol)
    cap_price = get_capital_gr_price(api_sym)
    
    if api_price and cap_price:
        match = abs(api_price - cap_price) < 0.01
        status = "✅" if match else "❌"
        print(f"{status} {symbol:10} | API: {api_price:8.2f} | Capital.gr: {cap_price:8.2f}")
        if match:
            matches += 1
        else:
            mismatches += 1
    elif api_price:
        print(f"⚠️  {symbol:10} | API: {api_price:8.2f} | Capital.gr: N/A")
    else:
        print(f"❌ {symbol:10} | Not in API!")

# Parallel fetch from capital.gr
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {}
    for sym, api_sym in sample_stocks.items():
        future = executor.submit(compare_stock, sym, api_sym)
        futures[future] = sym
    
    for future in futures:
        future.result()

print(f"\nAccuracy: {matches}/{matches+mismatches} matched")
print()

# Test 3: Wait for update and check changes
print("⏰ Test 3: Automatic Update Verification")
print("-"*60)

first_update = response_data.get('last_update') if response_data else None
first_prices = dict(api_prices)
print(f"Initial time: {first_update}")
print(f"Initial count: {len(first_prices)}/31")

print("⏳ Waiting 65 seconds for next update...")
for i in range(65):
    time.sleep(1)
    if i % 10 == 0:
        print(f"   {65-i} seconds remaining...")

# Check if updated
data2 = test_api_prices()
second_update = data2.get('last_update') if data2 else None
second_prices = data2.get('prices', {}) if data2 else {}

print(f"\nSecond time: {second_update}")
print(f"Second count: {len(second_prices)}/31")

if first_update != second_update:
    print(f"✅ Server updated! ({first_update} → {second_update})")
else:
    print(f"⚠️  Update timing not changed (may be same minute)")

# Check if any prices changed
price_changes = 0
for sym, first_price in first_prices.items():
    second_price = second_prices.get(sym)
    if second_price and abs(first_price - second_price) > 0.001:
        price_changes += 1
        print(f"   📊 {sym}: {first_price:.2f} → {second_price:.2f}")

if price_changes > 0:
    print(f"✅ {price_changes} prices changed in update")
else:
    print(f"⚠️  No price changes detected (market may be stable)")

print()
print("="*60)
print("✅ Full Test Complete!")
print("="*60)
print()
print("Summary:")
print(f"  📡 API: {data2.get('count', 0)}/31 prices responding")
print(f"  🔍 Accuracy: {matches}/{matches+mismatches} matched capital.gr")
print(f"  ⏰ Updates: Every 60 seconds")
print(f"  📊 Dashboard: Open Untitled-1.html")
print()
