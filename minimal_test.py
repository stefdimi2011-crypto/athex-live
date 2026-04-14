#!/usr/bin/env python3
# Minimal test Flask app
from flask import Flask, jsonify

app = Flask(__name__)

# Store test data on the app instance
app.data = {
    'message': 'Hello',
    'count': 42
}

@app.route('/test', methods=['GET'])
def test():
    print(f"API called - returning data: {app.data}")
    return jsonify(app.data)

if __name__ == '__main__':
    print(f"Initial data: {app.data}")
    print("Server starting on http://127.0.0.1:5000/test")
    app.run(port=5000, debug=False, threaded=True)
