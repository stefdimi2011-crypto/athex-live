#!/usr/bin/env python3
import requests
import json
import time

time.sleep(2)

try:
    r = requests.get('http://127.0.0.1:5000/api/stocks', timeout=5)
    if r.status_code == 200:
        data = r.json()
        print("=" * 60)
        print("API /api/stocks Response:")
        print("=" * 60)
        if 'data' in data and 'MTLN' in data['data']:
            print("\nMTLN Stock Data:")
            print(json.dumps(data['data']['MTLN'], indent=2))
        else:
            print("No MTLN data found")
        
        print(f"\nTotal stocks: {data.get('count', 0)}")
        print(f"Last update: {data.get('lastUpdate', 'N/A')}")
    else:
        print(f"Error: {r.status_code}")
except Exception as e:
    print(f"Connection error: {e}")
