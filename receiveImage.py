import paho.mqtt.client as mqtt

QOS = 0
PORT = 1883
BROKER = 'mqtt.eclipse.org'
c = 0

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('Connected to',BROKER)
    else:
        print('Connection to',BROKER,'failed. Return code=',rc)
        os._exit(1)

def on_message(client, userdata, msg):
    global c
    c = c + 1
    print("Topic : ", msg.topic)
    print("writing " + str(c) + "files")
    with open("output.jpg", "wb") as f:
        f.write(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe("chrisNate/Image", qos=QOS)

client.loop_forever()