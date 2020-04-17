import cv2
from imutils.video import VideoStream
import time

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

vs = VideoStream(src=0).start()
time.sleep(2.0)

c = 0
framecounter = 0
print("detecting Faces")
while True:
    

    frame = vs.read()
    framecounter = framecounter + 1
    # print(framecounter)

    if (framecounter % 10000 == 0):
        # Convert into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        print("found {0} faces!".format(len(faces)))

        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

        if len(faces) > 0:
            print(c)
            c = c + 1
            status = cv2.imwrite('faces_detected' + str(c)  + '.jpg', frame)
            print ("Image faces_detected.jpg written to filesystem: ",status)