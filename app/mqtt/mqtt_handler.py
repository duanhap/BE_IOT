# app/mqtt/mqtt_handler.py

latest_data = {}

def on_connect(client, userdata, flags, rc):
    print("✔️ MQTT connected with result code:", rc)
    client.subscribe("#")  # Đăng ký mọi topic (hoặc list cụ thể)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    latest_data[topic] = payload
    print(f"📥 Topic: {topic} | Data: {payload}")

def get_latest_data(topic):
    return latest_data.get(topic, None)
