import os
import ssl
from typing import Any

import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv(
    "MQTT_HOST", "46439da5344d4e5381d171213726c721.s1.eu.hivemq.cloud"
)
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = "sonix"
MQTT_PASSWORD = "Pass1990"
MQTT_TLS_ENABLED = os.getenv("MQTT_TLS_ENABLED", "").lower() in {"1", "true", "yes"}

client = mqtt.Client()
client.reconnect_delay_set(min_delay=1, max_delay=30)
_TLS_CONFIGURED = False

# Nếu có username/password thì dùng
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


def _configure_tls() -> None:
    global _TLS_CONFIGURED
    if _TLS_CONFIGURED:
        return

    if MQTT_TLS_ENABLED or MQTT_PORT == 8883:
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)
        client.tls_insecure_set(False)
        _TLS_CONFIGURED = True


def connect() -> None:
    if client.is_connected():
        return

    _configure_tls()
    print(f"🔗 Connecting to MQTT broker {MQTT_HOST}:{MQTT_PORT} ...")
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

def _ensure_connection() -> None:
    if not client.is_connected():
        connect()


def publish(topic: str, payload: Any, qos: int = 0, retain: bool = False) -> None:
    _ensure_connection()
    result = client.publish(topic, payload, qos=qos, retain=retain)
    result.wait_for_publish()
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        raise RuntimeError(f"MQTT publish failed with code {result.rc}")


def subscribe(topic: str, qos: int = 0):
    _ensure_connection()
    print(f"📡 Subscribed: {topic}")
    client.subscribe(topic, qos)


def loop_forever():
    _ensure_connection()
    print("🚀 MQTT loop started.")
    client.loop_forever()