import time
import RPi.GPIO as GPIO

LED = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
for count in range(20):
    GPIO.output(LED, True)
    time.sleep(0.5)
    GPIO.output(LED, False)
    time.sleep(0.5)
print("Done!")
GPIO.cleanup()