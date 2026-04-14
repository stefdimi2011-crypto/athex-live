import requests
import time

time.sleep(3)
try:
    r = requests.get('http://127.0.0.1:5000/api/prices', timeout=3)
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Server running: {data.get('count', 0)} stocks")
    else:
        print(f"Server returned: {r.status_code}")
except Exception as e:
    print(f"❌ Could not connect: {e}")
