import os, json, random, string
from datetime import datetime
from config import config, ENVIRONMENT  # import config system

FLAG_DIR = "/var/lib/raspi-server"
DATA_FILE = os.path.join(FLAG_DIR, "data.json")


def generate_device_id(length=7):
    """Generate random alphanumeric device ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def log_and_store(message: str, data: dict):
    """Print to console and add to data.json log"""
    print(message)
    data.setdefault("logs", []).append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message
    })


def do_first_time_setup():
    os.makedirs(FLAG_DIR, exist_ok=True)

    install_data = {}
    if os.path.exists(DATA_FILE):
        # load existing data (so we don’t overwrite logs)
        with open(DATA_FILE, "r") as f:
            install_data = json.load(f)

    if "installed_at" not in install_data:
        install_data["installed_at"] = datetime.utcnow().isoformat() + "Z"
        log_and_store(f"Initialization complete, data written to {DATA_FILE}", install_data)

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
            "location": random.choice(["college", "universal", str(random.randint(100, 999))]),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        db.collection("devices").document(device_id).set(device_data)
        log_and_store(f"Device registered in Firestore with ID {device_id}", install_data)

    else:
        log_and_store(f"{DATA_FILE} already exists, skipping initialization", install_data)

    # Save back to file
    with open(DATA_FILE, "w") as f:
        json.dump(install_data, f, indent=2)


if __name__ == "__main__":
    do_first_time_setup()
