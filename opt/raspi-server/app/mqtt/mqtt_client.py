import paho.mqtt.client as mqtt
import threading
from flask import current_app
from .handlers.status import handle_status_all
from .handlers.execute import handle_execute
from .handlers.upload import handle_upload

# MQTT client instance (will be configured when app context is available)
mqtt_client = None
device_id = "U5401MlF6hZBmcjIFDHmnOlpFou1"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker")
        client.subscribe("status/all")
        client.subscribe(f"execute/{device_id}")
        client.subscribe(f"upload/{device_id}")
    else:
        print(f"❌ Failed to connect: {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    if topic == "status/all":
        handle_status_all(payload)

    elif topic.startswith("execute/"):
        handle_execute(client, device_id, payload)

    elif topic.startswith("upload/"):
        handle_upload(client, device_id, payload)

def init_mqtt_client(mqtt_broker, mqtt_port, mqtt_user, mqtt_pass):
    """Initialize MQTT client with provided configuration"""
    global mqtt_client
    
    if mqtt_client is None:
        # Create and configure MQTT client
        mqtt_client = mqtt.Client()
        if mqtt_user and mqtt_pass:
            mqtt_client.username_pw_set(mqtt_user, mqtt_pass)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        
        print(f"🔧 MQTT client initialized for broker: {mqtt_broker}:{mqtt_port}")
    
    return mqtt_client

def run_mqtt(mqtt_broker, mqtt_port, mqtt_user, mqtt_pass):
    """Run MQTT client in a loop"""
    if not mqtt_broker:
        print("❌ MQTT_BROKER not configured, skipping MQTT connection")
        return
    
    try:
        client = init_mqtt_client(mqtt_broker, mqtt_port, mqtt_user, mqtt_pass)
        client.connect(mqtt_broker, int(mqtt_port), 60)
        print(f"🔌 Connecting to MQTT broker at {mqtt_broker}:{mqtt_port}")
        client.loop_forever()
    except Exception as e:
        print(f"❌ MQTT connection error: {e}")

def start_mqtt(app=None):
    """Start MQTT client in a separate thread"""
    if app is None:
        # Try to use current_app if no app provided
        from flask import current_app
        app = current_app
    
    # Get configuration from Flask app
    with app.app_context():
        mqtt_broker = app.config.get("MQTT_BROKER")
        mqtt_port = app.config.get("MQTT_PORT", 1883)
        mqtt_user = app.config.get("MQTT_USER")
        mqtt_pass = app.config.get("MQTT_PASS")
    
    # Pass configuration to thread
    thread = threading.Thread(
        target=run_mqtt, 
        args=(mqtt_broker, mqtt_port, mqtt_user, mqtt_pass),
        daemon=True
    )
    thread.start()
    print("🚀 MQTT client thread started")
