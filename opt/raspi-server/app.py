#!/usr/bin/env python3
from flask import Flask, jsonify
import json, os

app = Flask(__name__)

FLAG_DIR = "/var/lib/raspi-server"
DATA_FILE = os.path.join(FLAG_DIR, "data.json")

@app.route("/")
def index():
    info = {"status": "running"}
    try:
        with open(DATA_FILE, "r") as f:
            info["initialized_data"] = json.load(f)
    except Exception:
        info["initialized_data"] = None
    return jsonify(info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
