import cv2
from imutils.video import VideoStream
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Constants
BROKER = '97.95.108.173'
PORT = 1883
QOS = 0
admitTrue = 16
admitFalse = 20


# Initialize GPIO input and output
GPIO.setmode(GPIO.BCM)
GPIO.setup(admitTrue, GPIO.OUT)
GPIO.setup(admitFalse, GPIO.OUT)
GPIO.output(admitTrue, False)
GPIO.output(admitFalse, False)



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

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    if msg.topic == "chrisNate/admit":
        print("Received message: LED = ", int(msg.payload))

    if(msg.topic == "chrisNate/admit"):
        if int(msg.payload) == 1:
            print("admitted")
            GPIO.output(admitTrue, True)
            GPIO.output(admitFalse, False)
        elif int(msg.payload) == 0:
            print("not admitted")
            GPIO.output(admitTrue, False)
            GPIO.output(admitFalse, True)   

# Setup MQTT client and callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("chrisNate/admit", qos=QOS)
client.loop_start()

def sendImage(image):
    client.publish('chrisNate/Image', image, 1)
    #TODO: fix so it doesnt loop forever but still sends the images
    client.loop_start()


# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

vs = VideoStream(src=0).start()

c = 0
framecounter = 0
print("detecting Faces")
try:
    while True:
        frame = vs.read()
        # Convert into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Draw rectangle around the faces
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

        if len(faces) > 0:
            print(c)
            c = c + 1
            print("Sending Image over mqtt")
            imgstr = cv2.imencode(".jpg", frame)[1].tostring()
            sendImage(bytearray(imgstr))
    
        time.sleep(4)
except KeyboardInterrupt:
    print("Done")
    GPIO.cleanup()
    client.disconnect()
