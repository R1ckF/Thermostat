from flask import Flask, request

import RPi.GPIO as GPIO
from thermostatCommands import *
import time
import logging
topPin = 2
bottomPin = 3
topButton = 4
bottomButton = 5

LOGGER = logging.getLogger()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		

	
    # while True:
    #    task = raw_input('Enter Up, Down or desired temperature: ')
    #    if task == 'Up':
    #        thermos.tempUp()
    #    elif task == 'Down':
    #        thermos.tempDown()
    #    elif task.isdigit():
    #        thermos.tempTarget = eval(task)
    #    else:
     #       print('Command not understood')
app = Flask(__name__)
app.config["DEBUG"] = True

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
			</body>
		</html>
	'''.format(temp=thermos.temp)
        
try:
    thermos = thermostat(topPin, bottomPin, topButton, bottomButton, LOGGER)
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
