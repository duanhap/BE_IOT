import os
from typing import List

from app.services.mqtt_service import handle_mqtt_message
from app.utils import mqtt_client

# Có thể override bằng env MQTT_SUB_TOPICS="iot/#,sensor/+/data"
SUB_TOPICS = os.getenv("MQTT_SUB_TOPICS", "iot/#")


def _parse_topics(raw: str) -> List[str]:
    return [topic.strip() for topic in raw.split(",") if topic.strip()]


def _on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("✅ Connected to MQTT broker.")
        for topic in _parse_topics(SUB_TOPICS):
            mqtt_client.subscribe(topic, qos=1)
    else:
        print(f"❌ MQTT connection failed: {reason_code}")


def _on_message(client, userdata, msg):
    print(f"📥 {msg.topic} -> {msg.payload}")
    try:
        handle_mqtt_message(msg.topic, msg.payload)
    except Exception as exc:
        print(f"❌ Error handling MQTT message: {exc}")


def start_mqtt():
    print("🚀 Starting MQTT listener...")

    mqtt_client.client.on_connect = _on_connect
    mqtt_client.client.on_message = _on_message
    mqtt_client.connect(start_loop=False)
    mqtt_client.loop_forever()