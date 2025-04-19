import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mqtt.example.com", 1883, 60)
client.publish("access_control", "OpenDoor")
