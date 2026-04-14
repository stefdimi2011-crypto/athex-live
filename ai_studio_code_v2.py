#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATHEX Live Stock Server
Ενημερώνει τιμές από capital.gr API κάθε 60 δευτερόλεπτα
"""

from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor, as_completed
import atexit
import time

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎯 ΑΡΧΙΚΟΠΟΙΗΣΗ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

app = Flask(__name__)
CORS(app)

# Κρυφή αποθήκη τιμών - GLOBAL για όλες τις αιτήσεις
CACHED_PRICES = {}
LAST_UPDATE = None
SESSION = requests.Session()

#Λίστα των 33+ έγκυρων ATHEX κωδικών
STOCKS = {
    "MTLN": "MTLN", "CENER": "CENER", "ALWN": "ALWN", "BOCHGR": "BOCHGR",
    "BYLOT": "BYLOT", "CNLCAP": "CNLCAP", "CREDIA": "CREDIA", "OPTIMA": "OPTIMA",
    "YKNOT": "YKNOT", "AAAK": "ΑΑΑΚ", "ADMIE": "ΑΔΜΗΕ", "ALPHA": "ΑΛΦΑ",
    "GEKT": "ΓΕΚΤΕΡΝΑ", "GMEZ": "ΓΚΜΕΖΖ", "DOMIK": "ΔΟΜΙΚ", "ETE": "ΕΤΕ",
    "EUROB": "ΕΥΡΩΒ", "IKTIN": "ΙΚΤΙΝ", "INLIF": "ΙΝΛΙΦ", "CAIROMEZ": "ΚΑΙΡΟΜΕΖ",
    "KEKR": "ΚΕΚΡ", "LAVI": "ΛΑΒΙ", "MATHIO": "ΜΑΘΙΟ", "MEVA": "ΜΕΒΑ",
    "MERKO": "ΜΕΡΚΟ", "MOI": "ΜΟΗ", "XYLP": "ΞΥΛΠ", "OTE": "ΟΤΕ",
    "PEIR": "ΠΕΙΡ", "PRD": "ΠΡΔ", "PRONTON": "ΠΡΟΝΤΕΑ", "ELITE": "ΕΛΙΤ",
    "AKAD": "ΑΚΑΔ"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 ΣΥΝΑΡΤΗΣΕΙΣ ΔΕΙΔΟΜΕΝΩΝ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_price(api_symbol: str) -> float:
    """Λαμβάνει μία τιμή και απο το capital.gr API"""
    try:
        url = f"https://www.capital.gr/api/quotes/{api_symbol}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = SESSION.get(url, headers=headers, timeout=5)
        data = resp.json()
        
        if data.get('ResultData'):
            result_data = data['ResultData']
            if isinstance(result_data, list) and len(result_data) > 0 and result_data[0]:
                quote = result_data[0]
                if isinstance(quote, dict) and quote.get('l'):
                    price = float(quote['l'])
                    print(f"  📈 {api_symbol}: {price}")
                    return price
    except Exception as e:
        print(f"  ❌ Error for {api_symbol}: {str(e)[:30]}")
    return None

def update_prices_background():
    """Ενημερώνει όλες τιες τιμές - καλείται κάθε 60 δευτερόλεπτα"""
    global CACHED_PRICES, LAST_UPDATE
    
    print(f"\n🔄 Ενημέρωση τιμών... {datetime.now().strftime('%H:%M:%S')}")
    print(f"   Cache BEFORE: {len(CACHED_PRICES)} items")
    updated_count = 0
    
    # Parallel requests με ThreadPool - 10 ταυτόχρονα requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_price, api_sym): sym_code 
                   for sym_code, api_sym in STOCKS.items()}
        
        for future in as_completed(futures):
            symbol = futures[future]
            try:
                price = future.result()
                if price is not None and price > 0:
                    print(f"   💾 Saving {symbol}={price}")
                    CACHED_PRICES[symbol] = price
                    updated_count += 1
            except Exception as e:
                print(f"   Error for {symbol}: {e}")
    
    LAST_UPDATE = datetime.now().strftime('%H:%M:%S')
    print(f"   Cache AFTER: {len(CACHED_PRICES)} items")
    print(f"✅ Ενημερώθηκαν {updated_count}/{len(STOCKS)} μετοχές")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🌐 FLASK ENDPOINTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/api/prices', methods=['GET'])
def api_prices():
    """Επιστρέφει όλες τις τιμές (cached)"""
    return jsonify({
        "prices": CACHED_PRICES,
        "last_update": LAST_UPDATE,
        "count": len(CACHED_PRICES),
        "total_stocks": len(STOCKS)
    })

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ATHEX Live Stock Server")
    print("=" * 60)
    
    # Εργολαβία: αρχική ενημέρωση
    print("\n⏳ Αρχική λήψη τιμών...")
    update_prices_background()
    
    # APScheduler: Ενημέρωση κάθε 60 δευτερόλεπτα
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=update_prices_background,
        trigger="interval",
        seconds=60,
        id='price_update_job'
    )
    scheduler.start()
    print("✅ Background scheduler ενεργοποιήθηκε (κάθε 60 δευτερόλεπτα)")
    
    # Cleanup on exit
    atexit.register(lambda: scheduler.shutdown())
    
    # Flask info
    print(f"\n📊 Server: http://127.0.0.1:5000/api/prices")
    print(f"💾 Stocks cached: {len(STOCKS)}")
    print(f"⏹️  Σταμάτημα: CTRL+C\n")
    
    # Ξεκινά τον Flask server
    app.run(port=5000, debug=False, use_reloader=False, threaded=True)
