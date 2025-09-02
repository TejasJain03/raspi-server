#!/usr/bin/env python3
"""
One-time initialization script for raspi-server.
Creates /var/lib/raspi-server/data.json safely.
"""

import os, json
from datetime import datetime

FLAG_DIR = "/var/lib/raspi-server"
DATA_FILE = os.path.join(FLAG_DIR, "data.json")

def do_first_time_setup():
    # Create directory with correct permissions
    os.makedirs(FLAG_DIR, exist_ok=True)
    
    # Prepare initial data
    data = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "message": "Raspberry Pi server initialized on first install",
        "example": True
    }

    # Only write file if it doesn’t exist
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Initialization complete, data written to {DATA_FILE}")
    else:
        print(f"{DATA_FILE} already exists, skipping initialization")

if __name__ == "__main__":
    do_first_time_setup()
