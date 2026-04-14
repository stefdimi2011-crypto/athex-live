#!/usr/bin/env python3
# ATHEX Live Stock Server - Simplified version
# python ai_studio_code_simple.py

from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor, as_completed
import atexit

app = Flask(__name__)
CORS(app)

# Store prices in a simple in-memory store
app.prices_data = {
    'prices': {},
    'last_update': None
}

SESSION = requests.Session()

STOCKS = {
    "MTLN": "MTLN", "CENER": "CENER", "ALWN": "ALWN", "BOCHGR": "BOCHGR",
    "BYLOT": "BYLOT", "CNLCAP": "CNLCAP", "CREDIA": "CREDIA", "OPTIMA": "OPTIMA",
    "YKNOT": "YKNOT", "AAAK": "ΑΑΑΚ", "ADMIE": "ΑΔΜΗΕ", "ALPHA": "ΑΛΦΑ",
    "GEKT": "ΓΕΚΤΕΡΝΑ", "GMEZ": "ΓΚΜΕΖΖ", "DOMIK": "ΔΟΜΙΚ", "ETE": "ΕΤΕ",
    "EUROB": "ΕΥΡΩΒ", "IKTIN": "ΙΚΤΙΝ", "INLIF": "ΙΝΛΙΦ", "CAIROMEZ": "ΚΑΙΡΟΜΕΖ",
    "KEKR": "ΚΕΚΡ", "LAVI": "ΛΑΒΙ", "MATHIO": "ΜΑΘΙΟ", "MEVA": "ΜΕΒΑ",
    "MERKO": "ΜΕΡΚΟ", "MOI": "ΜΟΗ", "XYLP": "ΞΥΛΠ", "OTE": "ΟΤΕ",
    "PEIR": "ΠΕΙΡ", "PRD": "ΠΡΔ", "PRONTON": "ΠΡΟΝΤΕΑ"
}

def get_price(api_symbol: str) -> float:
    try:
        url = f"https://www.capital.gr/api/quotes/{api_symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = SESSION.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data.get('ResultData') and isinstance(data['ResultData'], list) and len(data['ResultData']) > 0:
            if data['ResultData'][0] and data['ResultData'][0].get('l'):
                return float(data['ResultData'][0]['l'])
    except:
        pass
    return None

def update_prices():
    print(f"\n🔄 Update... {datetime.now().strftime('%H:%M:%S')}")
    
    new_prices = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_price, api_sym): sym for sym, api_sym in STOCKS.items()}
        for future in as_completed(futures):
            sym = futures[future]
            price = future.result()
            if price:
                new_prices[sym] = price
    
    # Store directly to app object
    print(f"  Storing {len(new_prices)} prices...")
    app.prices_data['prices'] = new_prices
    app.prices_data['last_update'] = datetime.now().strftime('%H:%M:%S')
    print(f"  ✅ Stored. Read back: {len(app.prices_data['prices'])} items")
    print(f"✅ Updated {len(new_prices)}/{len(STOCKS)}")

@app.route('/api/prices', methods=['GET'])
def api_prices():
    data = app.prices_data
    print(f"\n📡 API request - Returning {len(data['prices'])} prices")
    return jsonify({
        "prices": data['prices'],
        "last_update": data['last_update'],
        "count": len(data['prices'])
    })

if __name__ == '__main__':
    print("="*50)
    print("🚀 ATHEX Live Stock Server (Simplified)")
    print("="*50)
    
    print("\n⏳ Initial update...")
    update_prices()
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_prices, trigger="interval", seconds=60)
    scheduler.start()
    print("✅ Updates every 60 seconds\n")
    
    atexit.register(lambda: scheduler.shutdown())
    
    print("Server: http://127.0.0.1:5000/api/prices")
    print("Press CTRL+C to stop\n")
    
    app.run(port=5000, debug=False, use_reloader=False, threaded=True)
