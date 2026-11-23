import paho.mqtt.client as mqtt
import ssl
import random
import string

def generate_client_id(prefix):
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}-{random_suffix}"

broker = "localhost"
port = 8883
topic = "iot/lab/temperature"
username = "sub_user"
password = "SubPass123!"
ca_cert = r"C:\Program Files\mosquitto\certs\ca.crt"
client_id = generate_client_id("subscriber")

print(f"Subscriber ON (TLS) - Client ID: {client_id}")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker securely (TLS)")
        client.subscribe(topic, qos=1)
    else:
        print(f"Connection failed with code {reason_code}")

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    for rc in reason_code_list:
        if rc.is_failure:
            print(f"Subscription DENIED by ACL (reason code: {rc})")
        else:
            print(f"Subscription granted with QoS: {rc.value}")

def on_message(client, userdata, msg):
    print(f"Received on {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(
    client_id=client_id,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.username_pw_set(username, password)
client.tls_set(ca_certs=ca_cert, tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(broker, port)
client.loop_forever()