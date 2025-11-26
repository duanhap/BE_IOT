# app/mqtt/mqtt_service.py
from .mqtt_client import get_mqtt_client
from .mqtt_handler import on_connect, on_message

def start_mqtt():
    client = get_mqtt_client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()
    return client

def publish(topic, message):
    client = get_mqtt_client()
    client.publish(topic, message)
    print(f"📤 Sent to {topic}: {message}")
