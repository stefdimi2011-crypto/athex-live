#!/usr/bin/env python3
"""
ATHEX Live Server Launcher
Starts the stock price server and opens the dashboard
"""

import subprocess
import webbrowser
import time
import sys
import os
import shutil
from pathlib import Path

def start_server():
    """Start the Flask server silently in background"""
    server_path = Path(__file__).parent / "ai_studio_code.py"
    
    if not server_path.exists():
        return None
    
    try:
        # Start server silently in background (no window)
        if sys.platform == 'win32':
            # Use DETACHED_PROCESS to hide window (Windows only)
            process = subprocess.Popen(
                f'python "{server_path}"',
                shell=True,
                creationflags=0x00000008,  # DETACHED_PROCESS
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # For other systems
            process = subprocess.Popen(
                [sys.executable, str(server_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        return process
    except Exception as e:
        return None

def wait_for_server(max_wait=10):
    """Wait for server to be ready (silently)"""
    import socket
    
    for i in range(max_wait):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 5000))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        
        if i < max_wait - 1:
            time.sleep(1)
    
    return False

def open_dashboard():
    """Open the HTML dashboard in Chrome silently"""
    dashboard_path = Path(__file__).parent / "Untitled-1.html"
    
    if not dashboard_path.exists():
        return False
    
    try:
        file_url = dashboard_path.as_uri()
        
        # Try to open with Chrome specifically
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "chrome.exe"  # Fallback - search in PATH
        ]
        
        chrome_found = False
        for chrome_path in chrome_paths:
            if shutil.which(chrome_path) or os.path.exists(chrome_path):
                try:
                    subprocess.Popen([chrome_path, file_url], shell=False, 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
                    chrome_found = True
                    break
                except:
                    continue
        
        if not chrome_found:
            # Fallback to default browser if Chrome not found
            webbrowser.open(file_url)
        
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    # Start server silently
    start_server()
    
    # Wait for server to be ready
    wait_for_server()
    
    # Open dashboard and exit
    open_dashboard()
