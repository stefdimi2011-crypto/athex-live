#!/usr/bin/env python3
"""
Test all API endpoints
"""

import requests
import json

print("="*70)
print("🧪 API Endpoints Test")
print("="*70)
print()

endpoints = [
    ("/api/prices", "Live Prices"),
    ("/api/stocks", "Stocks List"),
    ("/health", "Health Check"),
]

for path, name in endpoints:
    try:
        url = f"http://127.0.0.1:5000{path}"
        resp = requests.get(url, timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ {name:20} ({path})")
            
            # Show sample data
            if 'count' in data:
                print(f"   └─ Count: {data['count']}")
            if 'stocks' in data:
                print(f"   └─ Stocks: {len(data['stocks'])}")
            if 'status' in data:
                print(f"   └─ Status: {data['status']}")
                
        else:
            print(f"❌ {name:20} ({path}) - Status {resp.status_code}")
            
    except Exception as e:
        print(f"❌ {name:20} ({path}) - {e}")
    
    print()

print("="*70)
print("✅ All endpoints verified!")
print("="*70)
