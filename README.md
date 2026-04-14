# ATHEX Live - Stock Market Dashboard 📊

Real-time ATHEX (Athens Stock Exchange) stock prices with beautiful modern dashboard. Data updated every 60 seconds from Capital.gr API.

## 🌐 Features

✅ Real-time stock prices (31 ATHEX stocks)  
✅ Automatic updates every 60 seconds  
✅ Beautiful responsive dashboard  
✅ Search and filter stocks  
✅ API endpoints for programmatic access  
✅ Works on desktop & mobile  
✅ Deploy to cloud with 1 click  

## 🚀 Quick Start (Local)

### Option 1: Double Click (Windows)
Simply double-click **`RUN_SERVER.bat`**

### Option 2: Command Line
```bash
python start.py
```

### Option 3: Manual
```bash
python ai_studio_code.py
```

Then open: **http://127.0.0.1:5000/**

## 📊 API Endpoints

- `GET /` - Main dashboard
- `GET /api/stocks` - Get all stocks with current prices
- `GET /api/prices` - Get all prices with detailed data
- `GET /api/history/<symbol>` - Get price history for a stock
- `GET /health` - Health check

## ☁️ Deploy to Cloud (Render)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `athex-live`
3. Click "Create repository"
4. Run these commands in your folder:
```bash
git add .
git commit -m "Initial commit - ATHEX Live Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/athex-live.git
git push -u origin main
```

### Step 2: Deploy to Render

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your `athex-live` repository
5. Fill in deployment settings:
   - **Name**: `athex-live`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn ai_studio_code:app`
6. Add environment variable:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.8`
7. Click "Deploy"

### Step 3: Share Your URL

After ~2-3 minutes, Render will give you a public URL like:
```
https://athex-live-xxxx.onrender.com
```

✅ Share this link and anyone can access your dashboard from phone/tablet without Python installed!

## 📱 Mobile Access

Once on Render, the dashboard is accessible from:
- 📱 Your phone
- 💻 Any computer
- 🌍 Anywhere in the world
- ⏰ 24/7 (automatic stock updates)

## 📁 Project Structure

```
athex-live/
├── ai_studio_code.py      # Flask server
├── start.py               # Launcher script
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── runtime.txt           # Python version
├── templates/
│   └── index.html        # Modern dashboard
└── README.md             # This file
```

## 🔧 Configuration

Edit `ai_studio_code.py` to modify:
- Update interval (currently 60 seconds)
- Port number (default 5000)
- Stock symbols
- API endpoints

## 📝 License

MIT

---

**ATHEX Live Dashboard** | Live from Greece 🇬🇷

## 🔌 API Endpoint

```
GET http://127.0.0.1:5000/api/prices
```

### Response
```json
{
  "count": 31,
  "last_update": "18:49:53",
  "prices": {
    "AAAK": 5.55,
    "ADMIE": 3.02,
    "ALPHA": 3.64,
    "ALWN": 14.4,
    "BOCHGR": 8.8,
    ...
  }
}
```

## 📈 Μετοχές που παρακολουθούνται (31)

**Latin symbols:** MTLN, CENER, ALWN, BOCHGR, BYLOT, CNLCAP, CREDIA, OPTIMA, YKNOT

**Greek symbols:** ΑΑΑΚ, ΑΔΜΗΕ, ΑΛΦΑ, ΓΕΚΤΕΡΝΑ, ΓΚΜΕΖΖ, ΔΟΜΙΚ, ΕΤΕ, ΕΥΡΩΒ, ΙΚΤΙΝ, ΙΝΛΙΦ, ΚΑΙΡΟΜΕΖ, ΚΕΚΡ, ΛΑΒΙ, ΜΑΘΙΟ, ΜΕΒΑ, ΜΕΡΚΟ, ΜΟΗ, ΞΥΛΠ, ΟΤΕ, ΠΕΙΡ, ΠΡΔ, ΠΡΟΝΤΕΑ

## ⏸️ Σταμάτημα

Κλείστε το σερβερ window ή πατήστε Ctrl+C

## 🔧 Τεχνική

- **Framework:** Flask 2.3.2
- **Scheduler:** APScheduler (background updates κάθε 60 δευτερόλεπτα)
- **Data Source:** capital.gr JSON API
- **Concurrency:** ThreadPoolExecutor για παράλληλες request

---
**Status:** ✅ Production Ready
