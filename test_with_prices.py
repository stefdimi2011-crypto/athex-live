#!/usr/bin/env python3
# Test Flask app with stock price fetching
from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Store prices on app instance
app.prices_data = {
    'prices': {},
    'last_update': None,
    'test_count': 0
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

def fetch_test():
    print("⏳ Fetching prices...")
    new_prices = {}
    for sym, api_sym in STOCKS_SMALL.items():
        price = get_price(api_sym)
        if price:
            new_prices[sym] = price
            print(f"  ✅ {sym}: {price}")
    
    print(f"\n💾 Storing {len(new_prices)} prices to app...")
    app.prices_data['prices'] = new_prices
    app.prices_data['test_count'] += 1
    print(f"App now has: prices={len(app.prices_data['prices'])}, test_count={app.prices_data['test_count']}")

@app.route('/api/prices', methods=['GET'])
def api_prices():
    data = app.prices_data
    print(f"\n📡 API request - Reading from app: prices={len(data['prices'])}, test_count={data['test_count']}")
    return jsonify(data)

if __name__ == '__main__':
    print("=" * 50)
    print("Testing Flask + Stock Prices")
    print("=" * 50)
    
    fetch_test()
    
    print("\nServer starting on http://127.0.0.1:5000/api/prices\n")
    app.run(port=5000, debug=False, use_reloader=False, threaded=True)
