#!/usr/bin/env python3
"""
One-time initialization script. This is executed by the package
postinst only once (guarded by /var/lib/myflaskapp/.installed).
Place any setup logic here: seed DBs, create initial config, generate keys, etc.
"""

import json
import os
from datetime import datetime

FLAG_DIR = "/var/lib/raspi-server"
DATA_FILE = os.path.join(FLAG_DIR, "data.json")

def do_first_time_setup():
    os.makedirs(FLAG_DIR, exist_ok=True)
    data = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "welcome": "This was initialized during package installation.",
        "example_setting": True
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print("Wrote initial data to", DATA_FILE)

if __name__ == "__main__":
    do_first_time_setup()
