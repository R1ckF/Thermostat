import RPi.GPIO as GPIO
from thermostatCommands import *
import time
from flask import Flask, request

topPin = 2
bottomPin = 3
topButton = 4
bottomButton = 5

try:
    thermos = thermostat(topPin, bottomPin, topButton, bottomButton)
	
	
	
	while True:
		task = input('Enter Up, Down or desired temperature: ')
		if task == 'Up':
			thermos.tempUp()
		elif task == 'Down':
			thermos.tempDown()
		elif type(task) == int or type(task)==float:
			thermos.setTemp(task)
		else:
			print('Command not understood')
	
finally:
    GPIO.cleanup()


# app = Flask(__name__)
	# app.config["DEBUG"] = True

	# @app.route("/", methods=["GET", "POST"])
	# def mainpage():
		# return '''
			# <html>
				# <body>
					# <p>Current temp: {temp}
					# <form method="post" action="/Up">
						# <p><input type="submit" value="Up" /></p>
					# </form>
					# <form method="post" action="/Down">
						# <p><input type="submit" value="Down" /></p>
					# </form>
				# </body>
			# </html>
		# '''.format(temp=t.temp)
		
	# @app.route("/Up", methods=["GET", "POST"])
	# def Up():
		# thermos.up()
		# return '''
			# <html>
				# <body>
					# <p>Current temp: {temp}
					# <form method="post" action="/Up">
						# <p><input type="submit" value="Up" /></p>
					# </form>
					# <form method="post" action="/Down">
						# <p><input type="submit" value="Down" /></p>
					# </form>
				# </body>
			# </html>
		# '''.format(temp=t.temp)
		
	# @app.route("/Down", methods=["GET", "POST"])
	# def Down():
		# thermos.down()
		# return '''
			# <html>
				# <body>
					# <p>Current temp: {temp}
					# <form method="post" action="/Up">
						# <p><input type="submit" value="Up" /></p>
					# </form>
					# <form method="post" action="/Down">
						# <p><input type="submit" value="Down" /></p>
					# </form>
				# </body>
			# </html>
		# '''.format(temp=t.temp)
		
# class fakeThermos:
	# def __init__(self, temp):
		# self.temp=temp
	# def up(self):
		# self.temp+=0.5
	# def down(self):
		# self.temp-=0.5
# t = fakeThermos(2)
