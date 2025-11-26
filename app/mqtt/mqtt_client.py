# app/mqtt/mqtt_client.py
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

mqtt_client = None

def get_mqtt_client():
    global mqtt_client
    if mqtt_client is None:
        mqtt_client = mqtt.Client()
    return mqtt_client
