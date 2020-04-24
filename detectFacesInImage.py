import cv2
from imutils.video import VideoStream
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Constants
BROKER = '97.95.108.173'
BROKER = 'mqtt.eclipse.org'
PORT = 1883
QOS = 0
unlockedLED = 16
lockedLED = 20
DELAY = 2.0 # how long the lock stays unlocked

# Initialize GPIO input and output
GPIO.setmode(GPIO.BCM)
GPIO.setup(unlockedLED, GPIO.OUT)
GPIO.setup(lockedLED, GPIO.OUT)
GPIO.output(unlockedLED, False)
GPIO.output(lockedLED, False)

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

def blink(led):
    for count in range(5):
        GPIO.output(led, True)
        time.sleep(0.2)
        GPIO.output(led, False)
        time.sleep(0.2)

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    if msg.topic == "chrisNate/admit":
        print("Received message: LED = ", int(msg.payload))

    if(msg.topic == "chrisNate/admit"):
        if int(msg.payload) == 1:
            print("admitted")
            GPIO.output(unlockedLED, True)
            GPIO.output(lockedLED, False)

            #lock after timer has expired
            time.sleep(DELAY)
            GPIO.output(unlockedLED, False)
            GPIO.output(lockedLED, True)   
        elif int(msg.payload) == 0:
            print("not admitted")
            blink(lockedLED) 

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

        if len(faces) > 0:
            print(c)
            c = c + 1
            print("Sending Image over mqtt")
            imgstr = cv2.imencode(".jpg", frame)[1].tostring()
            sendImage(bytearray(imgstr))
    
        time.sleep(2)
except KeyboardInterrupt:
    print("Done")
    GPIO.cleanup()
    client.disconnect()
