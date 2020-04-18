import cv2
from imutils.video import VideoStream
import time
import paho.mqtt.client as mqtt


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

def sendImage(image):
    # with open("img.jpg", "rb") as image_file:
    #     content = image_file.read()
    bytesarray = image
    client.publish('chrisNate/Image', bytesarray, 0)

    client.loop_forever()


# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

vs = VideoStream(src=0).start()
time.sleep(2.0)

c = 0
framecounter = 0
print("detecting Faces")
while True:
    frame = vs.read()
    # Convert into grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # print("found {0} faces!".format(len(faces)))

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

    if len(faces) > 0:
        print(c)
        c = c + 1
        print("Sending Image over mqtt")
        imgstr = cv2.imencode(".jpg", frame)[1].tostring()
        sendImage(bytearray(imgstr))

        # print ("Image faces_detected.jpg written to filesystem: ",status)


