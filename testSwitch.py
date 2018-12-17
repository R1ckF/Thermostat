import RPi.GPIO as GPIO
import time

topPin = 22
bottomPin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(topPin, GPIO.OUT)
GPIO.setup(bottomPin, GPIO.OUT)


GPIO.output(bottomPin, GPIO.LOW)
GPIO.output(topPin, GPIO.LOW)


tStart = time.time()
def up():

	for i in range(5):
		GPIO.output(bottomPin, 1)
		time.sleep(1)
		GPIO.output(topPin, 1)
		time.sleep(1)
		GPIO.output(bottomPin, 0)
		time.sleep(1)
		GPIO.output(topPin, 0)
		time.sleep(1)
def down():

	for i in range(5):
		GPIO.output(topPin, 1)
		time.sleep(1)
		GPIO.output(bottomPin, 1)
		time.sleep(1)
		GPIO.output(topPin, 0)
		time.sleep(1)
		GPIO.output(bottomPin, 0)
		time.sleep(1)

down()
up()

GPIO.cleanup()
