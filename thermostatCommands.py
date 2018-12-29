import RPi.GPIO as GPIO
import logging
import time

"""
Control the set temp of thermostat
Bottom leads top, temp up
Top leads bottom, temp down
5.0 is min
35.0 is max
USES BCM NUMBERING!!
"""

class thermostat(object):

    def __init__(self, topPin, bottomPin, topButton, bottomButton, LOGGER, temp=16.0, sleepTime=0.3, bt=100):
        self.topPin = topPin
        self.bottomPin = bottomPin
        self.topButton = topButton
        self.bottomButton  = bottomButton
        self.temp = 16
        self.sleepTime = sleepTime
        self.min = 5.0
        self.max = 35.0
        self.bt = bt
        self.LOGGER = LOGGER
        self.tempTarget = temp
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.topPin, GPIO.OUT)
        GPIO.setup(self.bottomPin, GPIO.OUT)
        GPIO.setup(self.topButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bottomButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.bottomOff()
        self.topOff()
        self.initialize()
			
	
    @property
    def tempTarget(self):
        return self.__tempTarget

    @tempTarget.setter
    def tempTarget(self, tempTarget):
        if tempTarget < self.min:
            self.__tempTarget = self.min
            logging.info('Target temp to low, set to %s degrees instead', str(self.min))
        elif tempTarget > self.max:
            self.__tempTarget = self.max
            logging.info('Target temp to high, set to %s degrees instead', str(self.max))
        else:
            self.__tempTarget = tempTarget
            self.setTemp()
        
		
	
		
    def tempUp(self):
        if self.temp < self.max:
            if self.bottom == self.top:
                self.changePin(self.bottomPin)
            else:
                self.changePin(self.topPin)
            self.temp += 0.5
            logging.info('Temperature increased to %s degrees', str(self.temp))
            return True
        else:
            logging.info('Max temperature already reached')
            return False

    def tempDown(self):
        if self.temp > self.min:
            if self.top == self.bottom:
                self.changePin(self.topPin)
            else:
                self.changePin(self.bottomPin)
            self.temp -= 0.5
            logging.info('Temperature lowered to %s degrees', str(self.temp))
            return True
        else:
            logging.info('Minimum temperature already reached')
            return False
    
    def setTemp(self):
        if self.temp > self.tempTarget:
            while self.temp > self.tempTarget:
                self.tempDown()
        elif self.temp < self.tempTarget:
            while self.temp < self.tempTarget:
                self.tempUp()
        else:
            logging.debug('Temperature already at correct level')
        
    def initialize(self):
        # first check buttons
        self.topButtonStateOld = self.topButtonState()
        self.bottomButtonStateOld = self.bottomButtonState()

        self.LOGGER.info('Turn thermostat 2 clicks to check buttons are working')
        startloop = time.time()

        topButton, bottomButton, success = False, False, False
        while time.time()< startloop + 10:
            top, bottom = self.checkButtons()
            if not top:
                topButton = True
            if not bottom:
                bottomButton = True
            if topButton and bottomButton:
                success = True
                break
        if success:
            self.LOGGER.info("Buttons are recognized, adding triggers")
            self.addTriggers()
        else:
            self.LOGGER.warning("Buttons are not working, Testmode is activated")
            

        # secondly initialize temperature
        for i in range(40):
            self.tempDown()

        self.temp = self.min

        while self.temp < self.tempTarget:
            self.tempUp()

        self.LOGGER.info('Initialization complete, temperature set for %s degrees', str(self.temp))

        return True

    def controlButtons(self):
        if self.topButtonStateOld == self.bottomButtonStateOld:
            top, bottom = self.checkButtons()
            if not top:
                self.tempDown()
            elif not bottom:
                self.tempUp()
        else:
            top, bottom = self.checkButtons()
            if not top:
                self.tempUp()
            elif not bottom:
                self.tempDown()
        
        
            
        
        #Functions for internal use
    def addTriggers(self):
        #adding triggers for buttons
        GPIO.add_event_detect(self.topButton, GPIO.BOTH, callback=self.controlButtons, bouncetime=self.bt)
        GPIO.add_event_detect(self.bottomButton, GPIO.BOTH, callback=self.controlButtons, bouncetime=self.bt)
		
    def removeTriggers(self):
        #remove triggers for buttons
        GPIO.remove_event_detect(self.topButton)
        GPIO.remove_event_detect(self.bottomButton)
	
    def checkButtons(self):
        # returns true when state is similar to previous state for top and bottom pin
        if self.topButtonStateOld == self.topButtonState():
            top = True
        else:
            top = False
            self.topButtonStateOld = self.topButtonState()
        if self.bottomButtonStateOld == self.bottomButtonState():
            bottom = True
        else:
            bottom = False
            self.bottomButtonStateOld = self.bottomButtonState()
        return top, bottom
    
    def topButtonState(self):
        out =  GPIO.input(self.topButton)
        logging.debug('topButtonState: '+  str(out))
        return out

    def bottomButtonState(self):
        out =  GPIO.input(self.bottomButton)
        logging.debug('bottomButtonState: '+str(out))
        return out

    def topOn(self):
        logging.debug('topPin is 1')
        self.top = 1
        GPIO.output(self.topPin, 1)
        return True

    def topOff(self):
        logging.debug('topPin is 0')
        self.top = 0
        GPIO.output(self.topPin, 0)
        return True

    def bottomOn(self):
        logging.debug('bottomPin is 1')
        self.bottom = 1
        GPIO.output(self.bottomPin, 1)
        return True

    def bottomOff(self):
        logging.debug('bottomPin is 0')
        self.bottom = 0
        GPIO.output(self.bottomPin, 0)
        return True

    def changePin(self, pin):
        if pin == self.bottomPin:
            if self.bottom == 1:
                self.bottomOff()
                self.bottom = 0
            else:
                self.bottomOn()
                self.bottom = 1
        else:
            if self.top == 1:
                self.topOff()
                self.top = 0
            else:
                self.topOn()
                self.top = 1
        time.sleep(self.sleepTime)
        return True

    




