@echo off
chcp 65001 >nul
cls

REM ╔════════════════════════════════════════════════════════════════════╗
REM ║                                                                    ║
REM ║          📈 ATHEX LIVE STOCK PRICES - LAUNCHER 📈                ║
REM ║                     Double-Click Me!                             ║
REM ║                                                                    ║
REM ╚════════════════════════════════════════════════════════════════════╝

echo.
echo   🚀 Starting ATHEX Live Stock Server...
echo   ⏳ Please wait, opening your dashboard...
echo.

REM Activate virtual environment and start server
cd /d "%~dp0"
call .venv\Scripts\activate.bat

REM Start the server in background
start python ai_studio_code.py

REM Wait for server to start
timeout /t 3 /nobreak

REM Open browser to dashboard
start http://127.0.0.1:5000

REM Display info
echo.
echo   ✅ Server Started!
echo   📊 Dashboard opening in your browser...
echo   🔄 Live prices updating every 60 seconds
echo.
echo   📍 API: http://127.0.0.1:5000/api/prices
echo.
echo   💡 Keep this window open while server is running
echo.

pause
