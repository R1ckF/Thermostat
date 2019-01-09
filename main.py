from flask import Flask, request

import RPi.GPIO as GPIO
from thermostatCommands import *
import time
import logging
topPin = 13
bottomPin = 6
topButton = 26
bottomButton = 19

awayTemp = 12
homeTemp = 18
startTemp = 15

LOGGER = logging.getLogger()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
		
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
				<form method="post" action="/Home">
					<p><input type="submit" value="Home" /></p>
				</form>
				<form method="post" action="/Away">
					<p><input type="submit" value="Away" /></p>
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
				<form method="post" action="/Home">
					<p><input type="submit" value="Home" /></p>
				</form>
				<form method="post" action="/Away">
					<p><input type="submit" value="Away" /></p>
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
				<form method="post" action="/Home">
					<p><input type="submit" value="Home" /></p>
				</form>
				<form method="post" action="/Away">
					<p><input type="submit" value="Away" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)
 
@app.route("/Home", methods=["GET", "POST"])
def Home():
	thermos.home()
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
				<form method="post" action="/Home">
					<p><input type="submit" value="Home" /></p>
				</form>
				<form method="post" action="/Away">
					<p><input type="submit" value="Away" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)
	
@app.route("/Away", methods=["GET", "POST"])
def Away():
	thermos.away()
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
				<form method="post" action="/Home">
					<p><input type="submit" value="Home" /></p>
				</form>
				<form method="post" action="/Away">
					<p><input type="submit" value="Away" /></p>
				</form>
			</body>
		</html>
	'''.format(temp=thermos.temp)
 
 
        
try:
    thermos = thermostat(topPin, bottomPin, topButton, bottomButton, LOGGER, awayTemp = awayTemp, homeTemp = homeTemp, temp = startTemp)
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
