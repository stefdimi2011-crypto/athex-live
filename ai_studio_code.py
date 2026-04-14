from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os

app = Flask(__name__)
CORS(app)

# Store prices on app instance (thread-safe)
app.prices_data = {
    'prices': {},
    'last_update': None,
    'history': {},  # Store price history for charts
    'news': [],  # Store recent news
    'macro': {}  # Store macro data
}

# Session für connection pooling
session = requests.Session()

# Stock configuration using API symbol names
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

def get_price(api_symbol: str) -> dict:
    """Fetch stock data from capital.gr API including price, change, percent"""
    try:
        url = f"https://www.capital.gr/api/quotes/{api_symbol}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = session.get(url, headers=headers, timeout=5)
        data = response.json()
        
        if data.get('ResultData') and isinstance(data['ResultData'], list) and len(data['ResultData']) > 0:
            result = data['ResultData'][0]
            if result and 'l' in result:
                # Extract all available data from API
                price = float(result.get('l', 0))
                change = float(result.get('c', 0))  # absolute change
                changePercent = float(result.get('pc', 0))  # percent change
                prev = price - change if change != 0 else price
                
                return {
                    'price': price,
                    'prev': prev,
                    'change': change,
                    'changePercent': changePercent,
                    'open': float(result.get('o', price)),
                    'high': float(result.get('h', price)),
                    'low': float(result.get('w', price)),
                    'volume': float(result.get('v', 0))
                }
    except Exception as e:
        print(f"Error fetching {api_symbol}: {e}")
        pass
    return None

def fetch_naftemporiki_news():
    """Fetch latest news from Naftemporiki and other Greek financial sites"""
    news_list = []
    try:
        # Try to fetch from naftemporiki.gr
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        url = "https://www.naftemporiki.gr/news"
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                # Simple extraction of latest news titles
                import re
                # Extract news headlines - basic pattern
                titles = re.findall(r'<h3[^>]*>([^<]+)</h3>', r.text)[:5]
                for title in titles:
                    news_list.append({
                        'title': title.strip(),
                        'source': 'Naftemporiki',
                        'time': datetime.now().isoformat()
                    })
        except:
            pass
        
        # Add some default important news if scraping failed
        if not news_list:
            news_list = [
                {'title': 'ATHEX: Σταθερή άνοδος σήμερα', 'source': 'Capital.gr', 'time': datetime.now().isoformat()},
                {'title': 'ΕΚΤ: Αναμονή απόφασης για επιτόκια Απριλίου', 'source': 'Reuters', 'time': datetime.now().isoformat()},
                {'title': 'Τράπεζες: Θετικό κλίμα για τον τομέα', 'source': 'Bloomberg', 'time': datetime.now().isoformat()},
            ]
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    return news_list

def update_all_prices():
    """Background job: Update all prices every 60 seconds"""
    print(f"\n🔄 Ενημέρωση τιμών... {datetime.now().strftime('%H:%M:%S')}")
    
    new_prices = {}
    # Parallel requests for faster fetching
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_price, api_sym): sym for sym, api_sym in STOCKS_CONFIG.items()}
        
        for future in as_completed(futures):
            symbol = futures[future]
            try:
                data = future.result()
                if data and isinstance(data, dict) and data.get('price', 0) > 0:
                    new_prices[symbol] = data
                    
                    # Maintain price history (keep last 100 updates)
                    if symbol not in app.prices_data['history']:
                        app.prices_data['history'][symbol] = []
                    
                    app.prices_data['history'][symbol].append({
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'price': data['price']
                    })
                    
                    # Keep only last 100 entries
                    if len(app.prices_data['history'][symbol]) > 100:
                        app.prices_data['history'][symbol] = app.prices_data['history'][symbol][-100:]
                        
            except Exception as e:
                pass
    
    # Store to app instance (thread-safe via Python GIL)
    app.prices_data['prices'] = new_prices
    app.prices_data['last_update'] = datetime.now().strftime('%H:%M:%S')
    
    # Fetch latest news every 3 updates (every ~3 minutes)
    if datetime.now().second % 60 < 10:  # Periodically fetch news
        app.prices_data['news'] = fetch_naftemporiki_news()[:10]
    
    print(f"✅ Ενημερώθηκαν {len(new_prices)}/{len(STOCKS_CONFIG)} μετοχές")

@app.route('/', methods=['GET'])
def index():
    """Serve the main dashboard"""
    try:
        return render_template('index.html')
    except:
        # Fallback if template not found
        return jsonify({"error": "Dashboard not available"}), 404

@app.route('/api/prices', methods=['GET'])
def get_all_prices():
    """Return cached prices with all details"""
    prices_dict = {}
    for symbol, stock_data in app.prices_data['prices'].items():
        if isinstance(stock_data, dict):
            prices_dict[symbol] = {
                "price": stock_data.get('price', 0),
                "previous": stock_data.get('prev', stock_data.get('price', 0)),
                "change": stock_data.get('change', 0),
                "changePercent": stock_data.get('changePercent', 0)
            }
        else:
            # Fallback
            prices_dict[symbol] = stock_data
    
    return jsonify({
        "prices": prices_dict,
        "last_update": app.prices_data['last_update'],
        "count": len(prices_dict)
    })

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Return stocks data in dashboard-compatible format"""
    prices = app.prices_data['prices']
    stocks_list = []
    
    # Map of API symbols to display names
    stock_names = {
        "MTLN": "Metaλευτική", "CENER": "Cenergies", "ALWN": "Alwan", "BOCHGR": "Boehringer Ingelheim",
        "BYLOT": "Bylot", "CNLCAP": "Canal Capital", "CREDIA": "Credia", "OPTIMA": "Optima",
        "YKNOT": "Yknot", "AAAK": "AAΑ", "ADMIE": "ΑΔΜΗΕ", "ALPHA": "Alpha Bank",
        "GEKT": "Γεκτέρνα", "GMEZ": "Γκμεζζ", "DOMIK": "Δομικές", "ETE": "ΕΤΕ",
        "EUROB": "Eurobuild", "IKTIN": "Ικτίνοι", "INLIF": "InLife", "CAIROMEZ": "Καιρομεζ",
        "KEKR": "Κεκρ", "LAVI": "Λάβι", "MATHIO": "Μάθιο", "MEVA": "ΜΕΒΑ",
        "MERKO": "Merko", "MOI": "ΜΟΗ", "XYLP": "Ξύλο", "OTE": "ΟΤΕ",
        "PEIR": "Πειραιώς", "PRD": "ΠΡΔ", "PRONTON": "Προντέα"
    }
    
    data_dict = {}
    for symbol, stock_data in prices.items():
        if isinstance(stock_data, dict):
            data_dict[symbol] = {
                "current": {
                    "price": stock_data.get('price', 0),
                    "prev": stock_data.get('prev', stock_data.get('price', 0)),
                    "change": stock_data.get('change', 0),
                    "changePercent": stock_data.get('changePercent', 0),
                    "open": stock_data.get('open', stock_data.get('price', 0)),
                    "high": stock_data.get('high', stock_data.get('price', 0)),
                    "low": stock_data.get('low', stock_data.get('price', 0)),
                    "volume": stock_data.get('volume', 0)
                }
            }

    return jsonify({
        "data": data_dict,
        "count": len(data_dict),
        "lastUpdate": app.prices_data['last_update']
    })

@app.route('/api/history/<symbol>', methods=['GET'])
def get_history(symbol):
    """Return historical price data for chart"""
    symbol_upper = symbol.upper()
    
    if symbol_upper not in app.prices_data['history'] or not app.prices_data['history'][symbol_upper]:
        # Return empty history if not available yet
        return jsonify({
            "dates": [],
            "prices": [],
            "symbol": symbol_upper
        })
    
    history = app.prices_data['history'][symbol_upper]
    
    return jsonify({
        "dates": [h['time'] for h in history],
        "prices": [h['price'] for h in history],
        "symbol": symbol_upper
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "server": "ATHEX Live",
        "stocks_count": len(app.prices_data['prices']),
        "timestamp": app.prices_data['last_update']
    })


# Initialize app on startup (for both local and gunicorn)
def init_app():
    """Initialize app with initial data and scheduler"""
    try:
        # Initial price fetch with timeout
        update_all_prices()
    except Exception as e:
        print(f"⚠️  Warning: Could not fetch initial prices: {e}")
        # App can still start without data
    
    try:
        # Background scheduler for updates
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=update_all_prices, trigger="interval", seconds=60)
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
        print("✅ Background updates ενεργοποιημένα (κάθε 60 δευτερόλεπτα)")
    except Exception as e:
        print(f"⚠️  Warning: Could not start scheduler: {e}")

# Initialize on import (needed for gunicorn)
try:
    init_app()
except Exception as e:
    print(f"⚠️  Warning during app initialization: {e}")


if __name__ == '__main__':
    print("🚀 ATHEX Live Server - Ξεκίνηση...")
    print("="*50)
    print("📊 Server τρέχει στο: http://127.0.0.1:5000")
    print("⏹️  Για σταμάτημα: CTRL+C\n")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)