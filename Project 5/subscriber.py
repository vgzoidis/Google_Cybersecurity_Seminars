import paho.mqtt.client as mqtt
import random
import string

def generate_client_id(prefix):
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}-{random_suffix}"

broker = "localhost"
port = 1883
topic = "iot/temperature"
username = "sub_user"
password = "SubPass123!"
client_id = generate_client_id("subscriber")

print(f"Subscriber ON - Client ID: {client_id}")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker successfully")
        client.subscribe(topic, qos=0)
    else:
        print(f"Connection failed with code {reason_code}")

def on_message(client, userdata, msg):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(
    client_id=client_id,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_forever()