# app/mqtt_app.py
from app.utils.mqtt_client import start_mqtt
import time

def run():
    print("🚀 MQTT Worker Started...")
    start_mqtt()
    while True:
        time.sleep(1)
