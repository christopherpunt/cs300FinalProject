import base64
import random, string
import math
import paho.mqtt.client as mqtt
import json


QOS = 0
PORT = 1883
BROKER = 'mqtt.eclipse.org'


# Callback when a message is published
def on_publish(client, userdata, mid):
    print("MQTT data published")
# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('Connected to',BROKER)
    else:
        print('Connection to',BROKER,'failed. Return code=',rc)
        os._exit(1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(BROKER, PORT, 60)

with open("img.jpg", "rb") as image_file:
    content = image_file.read()
    bytesarray = bytearray(content)

print(type(bytesarray))
client.publish('chrisNate/Image', bytesarray, 0)

client.loop_forever()