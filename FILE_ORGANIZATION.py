#!/usr/bin/env python3
"""
FOLDER CLEANUP & ORGANIZATION
Shows which files you actually need
"""

print("\n")
print("="*70)
print("📁 FILE ORGANIZATION")
print("="*70)
print()

print("✅ ESSENTIAL FILES (Keep these)")
print("─"*70)

essential = {
    "RUN_SERVER.bat": "🎯 Main launcher - DOUBLE-CLICK THIS",
    "start.py": "🚀 Python launcher",
    "ai_studio_code.py": "📡 Flask server",
    "Untitled-1.html": "📊 Dashboard",
}

for file, desc in essential.items():
    print(f"  ✅ {file:30} {desc}")

print()

print("📚 DOCUMENTATION (Helpful)")
print("─"*70)

docs = {
    "README.md": "Full documentation",
    "QUICK_START.md": "Quick reference",
    "INDEX.md": "File directory",
    "requirements.txt": "Python dependencies",
}

for file, desc in docs.items():
    print(f"  📖 {file:30} {desc}")

print()

print("🧪 TESTING FILES (Optional)")
print("─"*70)

tests = [
    "FINAL_VERIFICATION.py",
    "validate_all_stocks.py",
    "test_endpoints.py",
    "test_dashboard.py",
    "comprehensive_test.py",
    "FINAL_REPORT.py",
]

for file in tests:
    print(f"  🧪 {file:30} Run to verify everything works")

print()

print("🗑️ DEVELOPMENT FILES (Can delete)")
print("─"*70)

dev_files = [
    "ai_studio_code (4).html",
    "ai_studio_code_final.py",
    "ai_studio_code_simple.py",
    "ai_studio_code_v2.py",
    "debug_scrape.py",
    "debug_selector.py",
    "explore_allstocks.py",
    "explore_structure.py",
    "extract_valid_stocks.py",
    "final_test.py",
    "find_api.py",
    "find_price_element.py",
    "fresh_test.py",
    "minimal_test.py",
    "SYSTEM_SUMMARY.py",
    "test_*.py",
]

for file in dev_files[:5]:
    print(f"  ❌ {file:30} Development/debug files")
print(f"  ❌ ... and {len(dev_files)-5} more debug files")

print()

print("="*70)
print("💡 RECOMMENDATION")
print("="*70)

print("""
You only NEED these 4 files:
  1. RUN_SERVER.bat
  2. start.py
  3. ai_studio_code.py
  4. Untitled-1.html

The rest are optional (documentation and testing).
You can delete all the debug/test files from development.

But it doesn't matter - they won't interfere with the server!
""")

print("="*70)
print()
