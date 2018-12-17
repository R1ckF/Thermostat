import RPi.GPIO as GPIO
from thermostatCommands import *
import time

topPin = 2
bottomPin = 3
topButton = 4
bottomButton = 5

try:
    thermos = thermostat(topPin, bottomPin, topButton, bottomButton)
    while True:
        thermos.controlButtons()
        time.sleep(1)




finally:
    GPIO.cleanup()
