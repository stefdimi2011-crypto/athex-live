import requests
import json
r = requests.get('http://127.0.0.1:5000/api/prices')
print(f'Status: {r.status_code}')
data = r.json()
print(f'Response: {json.dumps(data, indent=2, ensure_ascii=False)}')

