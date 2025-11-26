import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("localhost", 1883, 60)

client.publish("temperature_humidity", "25.8,45.2")
print("📤 Sent temperature_humidity: 25.8,45.2")

time.sleep(1)
client.disconnect()
