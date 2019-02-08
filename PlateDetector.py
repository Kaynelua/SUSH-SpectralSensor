import time
import RPi.GPIO as GPIO
import SpectralSensor as ss
import ProximitySensor as ps
from threading import Thread
import queue
import Servo as servo

GPIO.setmode(GPIO.BCM)

class PlateDetector():

	def __init__(self,mode='Train'):

		self.s = ss.SpectralSensor()
		self.p = ps.ProximitySensor()
		self.interruptPin = 17
		self.mode = 'Train'
		self.resultQueue = queue.Queue()
		self.p.setHighThreshold(10000)
		GPIO.setup(self.interruptPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(self.interruptPin,GPIO.FALLING,callback=self.sensorEvent)
		self.p.setInterrupt(1)

		self.refValues = {}

	def autoScanning(self):
		pass

	def train(self,c):
		val = pd.getResult()
		if c not in self.refValues.keys():
			self.refValues[c] = (val,1)
		else:
			(q,n) = self.refValues[c]
			newVal = q + (1/(n+1))*(val-q)
			self.refValues[c] = (newVal,n+1)




	def sensorEvent(self,pin):
		# Read Sensor and Store in Queue
		self.s.ledDrv(1)
		self.s.setBank(3)
		r = self.s.readAllCal()
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


count = 0
pd = PlateDetector()
while(True):
	try:
		#print(pd.getResult())
		#time.sleep(8)
		pd.train("Orange")
		print pd.refValues()
	except Exception, e:
    	print("Error : " + str(e))
		GPIO.cleanup()




'''
s = ss.SpectralSensor()
p = ps.ProximitySensor()


while(1):
        reading = p.readProximity()
         if(reading > 10000):
                s.ledDrv(1)
                s.setBank(3)
                r = s.readAllCal()
                s.ledDrv(0)
                print(r)
                dictData = {'sensorReadings':r}
                payload = json.dumps(dictData)
                MSG_INFO = client.publish("IC.Embedded/IOS/"+tableID,payload)
        time.sleep(0.1)
'''
