import paho.mqtt.client as mqtt
import ssl
import json
import time
import random
import uuid
from datetime import datetime, UTC

BROKER = "localhost"
PORT = 8883
TOPIC = "iot/lab/temperature"
CLIENT_ID = f"iot-publisher-{uuid.uuid4().hex[:8]}"
USERNAME = "pub_user"
PASSWORD = "PubPass123!"
CA_CERT = r"C:\Program Files\mosquitto\certs\ca.crt"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Publisher connected securely (TLS) with CLIENT_ID: {CLIENT_ID}")
    else:
        print(f"Failed to connect, return code {reason_code}")

client = mqtt.Client(
    client_id=CLIENT_ID,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(ca_certs=CA_CERT, tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.on_connect = on_connect
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

try:
    while True:
        payload = {
            "sensor_id": "temp_sensor",
            "temperature_c": round(random.uniform(20.0, 30.0), 2),
            "timestamp": datetime.now(UTC).isoformat()
        }
        client.publish(TOPIC, json.dumps(payload), qos=1)
        print(f"Published securely to {TOPIC}: {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stop publisher!")
    client.loop_stop()
    client.disconnect()