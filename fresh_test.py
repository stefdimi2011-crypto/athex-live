#!/usr/bin/env python3
import requests
import json

print("Making request to http://127.0.0.1:5000/api/prices")
try:
    response = requests.get('http://127.0.0.1:5000/api/prices', timeout=5)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response JSON:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
