import os
import ssl
from typing import Any

import paho.mqtt.client as mqtt

# -----------------------------
# CONFIG
# -----------------------------
MQTT_HOST = os.getenv(
    "MQTT_HOST", "46439da5344d4e5381d171213726c721.s1.eu.hivemq.cloud"
)
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "sonix")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "Pass1990")
MQTT_TLS_ENABLED = os.getenv("MQTT_TLS_ENABLED", "").lower() in {"1", "true", "yes"}

# -----------------------------
# GLOBAL CLIENT
# -----------------------------
client = mqtt.Client()
client.reconnect_delay_set(min_delay=1, max_delay=30)

_TLS_CONFIGURED = False


def _configure_tls() -> None:
    global _TLS_CONFIGURED
    if _TLS_CONFIGURED:
        return

    if MQTT_TLS_ENABLED or MQTT_PORT == 8883:
        client.tls_set(
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS_CLIENT
        )
        client.tls_insecure_set(False)
        _TLS_CONFIGURED = True


def connect(start_loop: bool = True) -> None:
    """Kết nối MQTT; có thể chọn loop_start hoặc không."""
    if client.is_connected():
        return

    _configure_tls()
    print(f"🔗 Connecting to MQTT broker {MQTT_HOST}:{MQTT_PORT} ...")

    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)

    if start_loop:
        client.loop_start()


def _ensure_connection() -> None:
    """Đảm bảo luôn kết nối ổn định."""
    if client.is_connected():
        return
    try:
        client.reconnect()
    except Exception:
        connect()


# -----------------------------
# PUBLISH
# -----------------------------
def publish(topic: str, payload: Any, qos: int = 0, retain: bool = False) -> None:
    """Publish an MQTT message safely."""
    _ensure_connection()
    result = client.publish(topic, payload, qos=qos, retain=retain)
    result.wait_for_publish()

    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        raise RuntimeError(f"MQTT publish failed with code {result.rc}")


# -----------------------------
# SUBSCRIBE
# -----------------------------
def subscribe(topic: str, qos: int = 0) -> None:
    _ensure_connection()
    print(f"📡 Subscribing: {topic}")
    client.subscribe(topic, qos)


# -----------------------------
# DEBUG LOG (OPTIONAL)
# -----------------------------
def enable_debug():
    client.on_log = lambda c, u, l, s: print("🐞 LOG:", s)


# -----------------------------
# BLOCKING LOOP (OPTIONAL)
# -----------------------------
def loop_forever() -> None:
    """Block current thread và xử lý MQTT traffic."""
    if not client.is_connected():
        # Khi dùng listener chuyên dụng, tránh loop_start trùng lặp.
        connect(start_loop=False)
    client.loop_forever()