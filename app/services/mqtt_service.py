# app/services/mqtt_service.py
import json
from datetime import datetime

# from app.repositories.device_history_repo import DeviceHistoryRepository
# from app.repositories.voice_history_repo import VoiceHistoryRepository
#
# device_repo = DeviceHistoryRepository()
# voice_repo = VoiceHistoryRepository()


def handle_mqtt_message(topic: str, payload: bytes):
    """Xử lý message nhận từ MQTT."""
    try:
        data = json.loads(payload.decode("utf-8"))
    except Exception:
        print("❌ Invalid JSON payload:", payload)
        return

    print(f"\n📨 [MQTT] Topic: {topic}")
    print("   Payload:", data)

    # # Example topic: iot/device/123/status
    # if topic.startswith("iot/device/"):
    #     device_id = topic.split("/")[2]
    #     device_repo.save_history(device_id, data)
    #     print(f"💾 Saved device history for {device_id}")
    #     return
    #
    # # Example topic: iot/voice/123
    # if topic.startswith("iot/voice/"):
    #     voice_id = topic.split("/")[2]
    #     voice_repo.save_voice(voice_id, data)
    #     print(f"💾 Saved voice history for {voice_id}")
    #     return
    #
    # print("⚠️ Unknown topic received:", topic)