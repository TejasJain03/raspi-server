#!/usr/bin/env python3
from flask import Flask, jsonify
import json, os, logging
from config import config, ENVIRONMENT

# Select config
app_config = config[ENVIRONMENT]()
app_config.init_firebase()

app = Flask(__name__)

FLAG_DIR = "/var/lib/raspi-server"
DATA_FILE = os.path.join(FLAG_DIR, "data.json")

@app.route("/")
def index():
    info = {"status": "running", "environment": ENVIRONMENT}
    try:
        with open(DATA_FILE, "r") as f:
            info["initialized_data"] = json.load(f)
    except FileNotFoundError:
        info["initialized_data"] = None
    except Exception as e:
        logging.exception("Error reading data.json")
        info["initialized_data"] = {"error": str(e)}
    return jsonify(info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
