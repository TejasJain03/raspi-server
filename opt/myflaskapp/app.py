#!/usr/bin/env python3
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

FLAG_DIR = "/var/lib/myflaskapp"
DATA_FILE = os.path.join(FLAG_DIR, "data.json")

@app.route("/")
def index():
    info = {"status": "running"}
    # attach info created during first-time init if present
    try:
        with open(DATA_FILE, "r") as f:
            info["initialized_data"] = json.load(f)
    except Exception:
        info["initialized_data"] = None
    return jsonify(info)

if __name__ == "__main__":
    # debug=False, host=0.0.0.0 so it's reachable on the network
    app.run(host="0.0.0.0", port=5000)
