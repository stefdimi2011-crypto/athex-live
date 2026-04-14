import requests
import json

# Test a few stock codes
test_stocks = ["MTLN", "CENER", "ALPHA", "OTE", "OPAP", "ADMIE"]

for symbol in test_stocks:
    url = f"https://www.capital.gr/api/quotes/{symbol}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        result_data = data.get('ResultData')
        print(f"\n{symbol}:")
        print(f"  ResultData type: {type(result_data)}")
        print(f"  ResultData value: {result_data}")
        
        if result_data:
            if isinstance(result_data, list) and len(result_data) > 0:
                print(f"  Price: {result_data[0].get('l')}")
            elif isinstance(result_data, dict):
                print(f"  Price: {result_data.get('l')}")
        else:
            print(f"  ERROR: ResultData is empty/None")
            
    except Exception as e:
        print(f"{symbol}: {e}")
