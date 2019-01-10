from flask import Flask, request

import RPi.GPIO as GPIO
from thermostatCommands import *
import time
import logging
topPin = 13
bottomPin = 6
topButton = 26
bottomButton = 19

OffTemp = 14.5
OnTemp = 18
startTemp = 15

LOGGER = logging.getLogger()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, filename='debug.log')

app = Flask(__name__)
app.config["DEBUG"] = False

@app.route("/", methods=["GET", "POST"])
def mainpage():
	return '''
		<html>
			<body>
				<p>Current temp: {temp}
				<form method="post" action="/Up">
					<p><input type="submit" value="Up" /></p>
				</form>
				<form method="post" action="/Down">
					<p><input type="submit" value="Down" /></p>
				</form>
				<form method="post" action="/On">
					<p><input type="submit" value="On" /></p>
				</form>
				<form method="post" action="/Off">
					<p><input type="submit" value="Off" /></p>
				</form>
				<form method="post" action="/Reset">
					<p><input type="submit" value="Reset" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)

@app.route("/Up", methods=["GET", "POST"])
def Up():
	thermos.tempUp()
	return '''
		<html>
			<body>
				<p>Current temp: {temp}
				<form method="post" action="/Up">
					<p><input type="submit" value="Up" /></p>
				</form>
				<form method="post" action="/Down">
					<p><input type="submit" value="Down" /></p>
				</form>
				<form method="post" action="/On">
					<p><input type="submit" value="On" /></p>
				</form>
				<form method="post" action="/Off">
					<p><input type="submit" value="Off" /></p>
				</form>
				<form method="post" action="/Reset">
					<p><input type="submit" value="Reset" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)

@app.route("/Down", methods=["GET", "POST"])
def Down():
	thermos.tempDown()
	return '''
		<html>
			<body>
				<p>Current temp: {temp}
				<form method="post" action="/Up">
					<p><input type="submit" value="Up" /></p>
				</form>
				<form method="post" action="/Down">
					<p><input type="submit" value="Down" /></p>
				</form>
				<form method="post" action="/On">
					<p><input type="submit" value="On" /></p>
				</form>
				<form method="post" action="/Off">
					<p><input type="submit" value="Off" /></p>
				</form>
				<form method="post" action="/Reset">
					<p><input type="submit" value="Reset" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)

@app.route("/On", methods=["GET", "POST"])
def On():
	thermos.on()
	return '''
		<html>
			<body>
				<p>Current temp: {temp}
				<form method="post" action="/Up">
					<p><input type="submit" value="Up" /></p>
				</form>
				<form method="post" action="/Down">
					<p><input type="submit" value="Down" /></p>
				</form>
				<form method="post" action="/On">
					<p><input type="submit" value="On" /></p>
				</form>
				<form method="post" action="/Off">
					<p><input type="submit" value="Off" /></p>
				</form>
				<form method="post" action="/Reset">
					<p><input type="submit" value="Reset" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)

@app.route("/Off", methods=["GET", "POST"])
def Off():
	thermos.off()
	return '''
		<html>
			<body>
				<p>Current temp: {temp}
				<form method="post" action="/Up">
					<p><input type="submit" value="Up" /></p>
				</form>
				<form method="post" action="/Down">
					<p><input type="submit" value="Down" /></p>
				</form>
				<form method="post" action="/On">
					<p><input type="submit" value="On" /></p>
				</form>
				<form method="post" action="/Off">
					<p><input type="submit" value="Off" /></p>
				</form>
				<form method="post" action="/Reset">
					<p><input type="submit" value="Reset" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)

@app.route("/Reset", methods=["GET", "POST"])
def Reset():
	thermos.reset()
	return '''
		<html>
			<body>
				<p>Current temp: {temp}
				<form method="post" action="/Up">
					<p><input type="submit" value="Up" /></p>
				</form>
				<form method="post" action="/Down">
					<p><input type="submit" value="Down" /></p>
				</form>
				<form method="post" action="/On">
					<p><input type="submit" value="On" /></p>
				</form>
				<form method="post" action="/Off">
					<p><input type="submit" value="Off" /></p>
				</form>
				<form method="post" action="/Reset">
					<p><input type="submit" value="Reset" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)



try:
    thermos = thermostat(topPin, bottomPin, topButton, bottomButton, LOGGER, offTemp = OffTemp, onTemp = OnTemp, temp = startTemp)
    app.run(host='0.0.0.0',port=5000)

finally:
    print('Error occurred, clean GPIOs')
    GPIO.cleanup()


#

# class fakeThermos:
	# def __init__(self, temp):
		# self.temp=temp
	# def up(self):
		# self.temp+=0.5
	# def down(self):
		# self.temp-=0.5
# t = fakeThermos(2)
