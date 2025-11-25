def start_mqtt():
    # app/mqtt_app.py
    from app.utils.mqtt_client import client, connect, subscribe, loop_forever
    from app.services.mqtt_service import handle_mqtt_message
import os
from typing import List

from app.services.mqtt_service import handle_mqtt_message
from app.utils import mqtt_client

SUB_TOPICS = os.getenv("MQTT_SUB_TOPICS", "iot/#")


def _parse_topics(config: str) -> List[str]:
    return [topic.strip() for topic in config.split(",") if topic.strip()]


def _on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("✅ MQTT connected successfully.")
        for topic in _parse_topics(SUB_TOPICS):
            mqtt_client.subscribe(topic, qos=1)
    else:
        print(f"❌ MQTT connection failed: {reason_code}")


def _on_message(client, userdata, msg):
    handle_mqtt_message(msg.topic, msg.payload)


def start_mqtt():
    mqtt_client.client.on_connect = _on_connect
    mqtt_client.client.on_message = _on_message
    mqtt_client.connect()
    mqtt_client.loop_forever()
    # Các topic bạn muốn subscribe
    SUB_TOPICS = [
        ("iot/device/+", 0),
        ("iot/voice/+", 0),
    ]

    def start_mqtt():
        print("🚀 Starting MQTT service...")

        # Gán callback
        client.on_connect = on_connect
        client.on_message = on_message

        # Kết nối broker
        connect()

        # Subscribe topic
        for topic, qos in SUB_TOPICS:
            subscribe(topic, qos)

        # Chạy vòng lặp
        loop_forever()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✅ MQTT Connected successfully!")
        else:
            print(f"❌ MQTT Connection failed with code {rc}")

    def on_message(client, userdata, msg):
        try:
            handle_mqtt_message(msg.topic, msg.payload)
        except Exception as e:
            print("❌ Error handling MQTT message:", e)