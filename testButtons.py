import RPi.GPIO as GPIO
import time

topPin = 22
bottomPin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(topPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(bottomPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bottomStatePrev = GPIO.input(bottomPin)
topStatePrev = GPIO.input(topPin)

print "bottomState: ", bottomStatePrev
print "topState: ",  topStatePrev

tStart = time.time()

while time.time()-tStart < 30:
	bottomState = GPIO.input(bottomPin)
	topState = GPIO.input(topPin)
 
	if bottomState != bottomStatePrev:
		bottomStatePrev = bottomState
		print "BottomPin is now ", bottomState
	if  topState != topStatePrev:
		topStatePrev = topState
		print "TopPin is now ", topState
	time.sleep(0.1)
GPIO.cleanup()
