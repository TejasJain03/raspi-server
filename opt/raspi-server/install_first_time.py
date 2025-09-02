#!/usr/bin/env python3
"""
One-time initialization script. This runs during .deb install
and only once (guarded by /var/lib/raspi-server/.installed).
"""

import os, json
from datetime import datetime

FLAG_DIR = "/raspi-server"
DATA_FILE = os.path.join(FLAG_DIR, "data.json")

def do_first_time_setup():
    os.makedirs(FLAG_DIR, exist_ok=True)
    data = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "message": "Raspberry Pi server initialized on first install",
        "example": True
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print("Initialization complete, data written to", DATA_FILE)

if __name__ == "__main__":
    do_first_time_setup()
