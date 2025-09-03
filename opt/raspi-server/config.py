# config.py
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

# Step 1: Load .env to know which environment is active
load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# Step 2: Load environment-specific file
env_file = f".env.{ENVIRONMENT}"
if os.path.exists(env_file):
    load_dotenv(env_file, override=True)
    print(f"✅ Loaded environment variables from {env_file}")
else:
    raise FileNotFoundError(f"Environment file {env_file} not found")

class Config:
    """Base configuration"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    FIREBASE_SERVICE_ACCOUNT_PATH = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")

    @staticmethod
    def init_firebase():
        """Initialize Firebase Admin SDK using service account JSON"""
        service_account_path = Config.FIREBASE_SERVICE_ACCOUNT_PATH
        if not service_account_path:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_PATH is not set in environment variables.")

        if not os.path.exists(service_account_path):
            raise FileNotFoundError(f"Service account file not found at {service_account_path}")

        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            print(f"✅ Firebase initialized with service account {service_account_path}")

        return True


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
