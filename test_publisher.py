import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("localhost", 1883, 60)

client.publish("temperature", "30.8")
print("📤 Sent temperature: 26.8")

time.sleep(1)
client.disconnect()
