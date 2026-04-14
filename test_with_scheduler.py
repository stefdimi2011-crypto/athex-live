#!/usr/bin/env python3
# Test Flask + APScheduler background updates
from flask import Flask, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import atexit
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Store prices on app instance
app.prices_data = {
    'prices': {},
    'last_update': None,
}

STOCKS_SMALL = {
    "MTLN": "MTLN", 
    "CENER": "CENER",
    "ALWN": "ALWN"
}

def get_price(api_symbol: str) -> float:
    try:
        url = f"https://www.capital.gr/api/quotes/{api_symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data.get('ResultData') and len(data['ResultData']) > 0:
            if data['ResultData'][0] and data['ResultData'][0].get('l'):
                return float(data['ResultData'][0]['l'])
    except:
        pass
    return None

def update_prices():
    """Called by background scheduler"""
    print(f"\n🔄 Background update at {datetime.now().strftime('%H:%M:%S')}")
    new_prices = {}
    for sym, api_sym in STOCKS_SMALL.items():
        price = get_price(api_sym)
        if price:
            new_prices[sym] = price
    
    print(f"  Fetched {len(new_prices)} prices")
    print(f"  Before assignment: app.prices_data['prices'] has {len(app.prices_data['prices'])} items")
    app.prices_data['prices'] = new_prices
    app.prices_data['last_update'] = datetime.now().strftime('%H:%M:%S')
    print(f"  After assignment: app.prices_data['prices'] has {len(app.prices_data['prices'])} items")

@app.route('/api/prices', methods=['GET'])
def api_prices():
    print(f"\n📡 API: Reading prices - {len(app.prices_data['prices'])} items, last_update={app.prices_data['last_update']}")
    return jsonify(app.prices_data)

if __name__ == '__main__':
    print("=" * 50)
    print("APScheduler + Flask Test")
    print("=" * 50)
    
    print("\n⏳ Initial fetch...")
    update_prices()
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_prices, trigger="interval", seconds=5)
    scheduler.start()
    print("✅ Background scheduler started (5-second updates)\n")
    
    atexit.register(lambda: scheduler.shutdown())
    
    print("Server starting: http://127.0.0.1:5000/api/prices\n")
    app.run(port=5000, debug=False, use_reloader=False, threaded=True)
