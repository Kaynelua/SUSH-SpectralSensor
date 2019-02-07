import time
import RPi.GPIO as GPIO
import SpectralSensor as ss
import ProximitySensor as ps
from threading import Thread
import queue
import Servo as servo

class PlateDetector():
	def __init__(self,mode='Train'):
		GPIO.setmode(GPIO.BCM)
		self.s = ss.SpectralSensor()
		self.p = ps.ProximitySensor()
		self.interruptPin = 17
		self.mode = 'Train'
		self.resultQueue = queue.Queue()
		GPIO.setup(self.interruptPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(self.interruptPin,GPIO.FALLING,callback=self.sensorEvent)
		self.p.setHighThreshold(10000)
		self.p.setInterrupt(1)

	def sensorEvent(self,pin):
		self.s.ledDrv(1)
		self.s.setBank(3)
		r = self.s.readAllCal()
		self.s.ledDrv(0)
		servo.open()
		time.sleep(0.1)
		servo.close()
		GPIO.remove_event_detect(self.interruptPin)
		self.p.setInterrupt(0)
		GPIO.add_event_detect(self.interruptPin,GPIO.FALLING,callback=self.sensorEvent)
#		self.p.setInterrupt(0)
		self.p.setInterrupt(1)
		self.resultQueue.put_nowait(r)
	def getResult(self):
		return self.resultQueue.get(block=True)

count = 0
pd = PlateDetector()
while(True):
	try:
		
		print(pd.getResult())
		print("yinghao senpai")
		time.sleep(8)
	except:
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
