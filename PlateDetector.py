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

GPIO.setmode(GPIO.BCM)

class PlateDetector():

	def __init__(self,mode='Train'):
		self.mode = 'Train'
		self.resultQueue = queue.Queue()
		self.refValues = self.loadReference()
		self.s = ss.SpectralSensor()
		self.p = ps.ProximitySensor()
		self.interruptPin = 17
		self.p.setHighThreshold(10000)
		GPIO.setup(self.interruptPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)	#sets up a hardware interrupt which is called when proximity sensor goes high
		GPIO.add_event_detect(self.interruptPin,GPIO.FALLING,callback=self.sensorEvent) # calls sensorEvent upon detection of interrupt
		self.p.setInterrupt(1)
		self.client = mq.Mqtt()

	def autoScanning(self):			
		#Gets the color(intensities at 6 different freq), convert to string representation and send it to MQTT broker
		res = self.getResult()
		colour = self.evalColour(res)
		print(colour)
		self.client.send("IC.Embedded/IOS/detection",colour)


	def train(self,c):		#Training the spectral sensor to convert intensities from 6 channels(F.P) to the name of the colour(string)
		val = pd.getResult()
		if c not in self.refValues.keys():
			self.refValues[c] = (val,1)
		else:
			(q,n) = self.refValues[c]
			newVal = q + (1/(n+1))*(val-q)
			self.refValues[c] = (newVal,n+1)

	def sensorEvent(self,pin):
		# Read Spectral Sensor and Store in Queue
		self.s.ledDrv(1)
		self.s.setBank(3)
		r = self.s.readAllCal()
		#Stores in queue immediately
		self.resultQueue.put_nowait(r)		
		self.s.ledDrv(0)
		# Open and Close to release plate
		servo.open()
		time.sleep(0.1)
		servo.close()
		# Reset Interrupt on Proximity Sensor
		GPIO.remove_event_detect(self.interruptPin)
		self.p.setInterrupt(0)
		GPIO.add_event_detect(self.interruptPin,GPIO.FALLING,callback=self.sensorEvent)
		self.p.setInterrupt(1)

	def getResult(self):
		return self.resultQueue.get(block=True)

	def evalColour(self,val):
		minError  = np.inf
		minColour = None
		for c in self.refValues.keys():
			(ref,n) = self.refValues[c]
			error = np.mean(((val-ref)**2))	#Use least square approach to decide which color the detected plate matches to from training data
			if(error < minError):
				minError = error
				minColour = c
		return minColour

	def store(self):	#Store training data into pickle file
		try:
			pickle.dump(self.refValues, open("data.pickle", "wb"))
		except Exception as e:
			print("Error :" + str(e))

		def loadReference(self):	#Loads training data into pickle file
		try:
			colourdict= pickle.load(open("data.pickle", "rb"))
			return colourdict
		except Exception as e:
			colourdict =  {} 
			return colourdict