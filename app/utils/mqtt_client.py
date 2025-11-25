# app/utils/mqtt_client.py
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "temperature"

latest_temperature = None  # Lưu tạm dữ liệu nhận được

def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global latest_temperature
    latest_temperature = msg.payload.decode()
    print(f"📥 Received Temperature: {latest_temperature}")

def get_latest_temperature():
    return latest_temperature

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()  # Chạy nền
    return client
