import time
import RPi.GPIO as GPIO
import SpectralSensor as ss
import ProximitySensor as ps
import Mqtt as mq
from threading import Thread
import queue
import Servo as servo
import numpy as np
import pickle
import PlateDetector as pd

GPIO.setmode(GPIO.BCM)

detector = pd.PlateDetector()
while(True):

	try:
		detector.autoScanning() #Runs the integrated process of entire system
		"""
		#Training to convert tuple of 6 f.p numbers to a string representing its color to minimize message length.	
		for i in range(0,5,1):
			detector.train("Red")
		for i in range(0,5,1):
			detector.train("Blue")
		for i in range(0,5,1):
			detector.train("White")
		for i in range(0,5,1):
			detector.train("Pink")
		for i in range(0,5,1):
			detector.train("Orange")
		detector.store()
		print(detector.evalColour(detector.getResult())) 		
		print(detector.refValues)
		"""	
	except Exception as e:
		print("Error : " + str(e))
		GPIO.cleanup()
