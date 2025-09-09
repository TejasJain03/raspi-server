from flask import Flask
from .config import Config
from app.mqtt.mqtt_client import start_mqtt
from app.errors import register_error_handlers

def create_app() -> Flask:
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config())

    # initialize mqtt client
    start_mqtt(app)

    # Errors
    register_error_handlers(app)

    return app
