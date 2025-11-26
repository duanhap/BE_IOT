# app/mqtt/mqtt_handler.py

from app.services.sensor_data_service import SensorDataService
from app.database.database import database  # <-- dùng instance database đã tạo
from sqlalchemy.orm import Session
import traceback

latest_data = {}

def on_connect(client, userdata, flags, rc):
    print("✔️ MQTT connected with result code:", rc)
    client.subscribe("#")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode().strip()
    latest_data[topic] = payload
    print(f"📥 Topic: {topic} | Data: {payload}")

    if topic == "temperature_humidity":
        try:
            temp_str, hum_str = payload.split(",")
            save_to_db(float(temp_str), float(hum_str))
        except Exception as e:
            print("⚠️ Error parsing MQTT payload:", e)
            traceback.print_exc()

def save_to_db(temperature: float, humidity: float):
    """Tự tạo và đóng session vì chạy ngoài FastAPI request."""
    db: Session = database.SessionLocal()  # ⬅ Dùng instance hiện có
    try:
        service = SensorDataService(db)
        service.save_sensor_data(temperature, humidity)
        print("💾 Saved to DB:", temperature, humidity)
    except Exception as e:
        print("⚠️ Database error:", e)
        traceback.print_exc()
    finally:
        db.close()

def get_latest_data(topic):
    return latest_data.get(topic, None)
