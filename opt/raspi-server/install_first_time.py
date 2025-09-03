import os, json, random, string
from datetime import datetime
from config import config, ENVIRONMENT  # import config system

FLAG_DIR = "/var/lib/raspi-server"
DATA_FILE = os.path.join(FLAG_DIR, "data.json")


def generate_device_id(length=7):
    """Generate random alphanumeric device ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def do_first_time_setup():
    os.makedirs(FLAG_DIR, exist_ok=True)

    # Only create file if it doesn’t exist
    if not os.path.exists(DATA_FILE):
        install_data = {
            "installed_at": datetime.utcnow().isoformat() + "Z"
        }
        with open(DATA_FILE, "w") as f:
            json.dump(install_data, f, indent=2)

        print(f"Initialization complete, data written to {DATA_FILE}")

        # ✅ Initialize Firebase using config
        app_config = config.get(ENVIRONMENT)
        app_config.init_firebase()

        from firebase_admin import firestore
        db = firestore.client()

        # Register in Firestore
        device_id = generate_device_id()
        device_data = {
            "device_ID": device_id,
            "status": "active",
            "assigned_status": "free",
            "location": random.choice(["college", "universal", str(random.randint(100,999))]),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        db.collection("devices").document(device_id).set(device_data)
        print(f"Device registered in Firestore with ID {device_id}")

    else:
        print(f"{DATA_FILE} already exists, skipping initialization")


if __name__ == "__main__":
    do_first_time_setup()
