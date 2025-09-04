import subprocess, os
from flask import Flask
import paho.mqtt.client as mqtt

app = Flask(__name__)

DEVICE_ID = "U5401MlF6hZBmcjIFDHmnOlpFou1"
BROKER = "64.227.185.157"
PORT = 1883

COMMAND_TOPIC = f"command/{DEVICE_ID}"
RESPONSE_TOPIC = f"response/{DEVICE_ID}"

mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Subscriber connected to MQTT broker")
        client.subscribe(COMMAND_TOPIC)
        print(f"📡 Subscribed to topic: {COMMAND_TOPIC}")
    else:
        print(f"❌ Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"📥 Received: {payload}")

    try:
        req_id, command = payload.split("|", 1)
    except ValueError:
        print("⚠️ Malformed payload")
        return

    # Process command and generate response
    response_message = f"{req_id}|OK: Received {command}"  # Default response

    # download the file using wget
    if command.startswith("LOAD "):
        url = command[5:].strip()
        filename = os.path.basename(url)
        local_path = f"/home/uttamthegoat/Documents/{filename}"

        result = subprocess.run(
            ["wget", "-O", local_path, url],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ Downloaded file: {local_path}")
            response_message = f"{req_id}|OK: Downloaded {local_path}"

            # run the file using quartus_pgm
            result = subprocess.run(
                ["quartus_pgm", "-c", "USB-Blaster [USB-0]", "-m", "jtag", "-o", f"p;{local_path}"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ Programmed file: {local_path}")
                # Include both stdout and stderr in the response
                output_logs = result.stdout
                if result.stderr:
                    output_logs += f"\nStderr: {result.stderr}"
                response_message = f"{req_id}|OK: Programming completed successfully\n{output_logs}"
            else:
                print(f"❌ Program failed: {result.stderr}")
                # Include both stdout and stderr for error case too
                error_logs = result.stderr
                if result.stdout:
                    error_logs = f"Stdout: {result.stdout}\nStderr: {error_logs}"
                response_message = f"{req_id}|ERROR: Programming failed\n{error_logs}"
        else:
            print(f"❌ Download failed: {result.stderr}")
            response_message = f"{req_id}|ERROR: {result.stderr}"

    response_topic = f"response/{DEVICE_ID}"
    client.publish(response_topic, response_message)
    print(f"➡️ Sent response: {response_message}")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()

@app.route("/")
def index():
    return "Subscriber running"


if __name__ == "__main__":
    app.run(port=5001)
