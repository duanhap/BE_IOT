# app/mqtt_app.py
from app.mqtt.mqtt_service import start_mqtt
import time

def run():
    print("🚀 MQTT Worker Started...")
    start_mqtt()
    while True:
        time.sleep(1)
