import time
import RPi.GPIO as GPIO
import SpectralSensor as ss
import ProximitySensor as ps
from threading import Thread
import Servo as servo

s = ss.SpectralSensor()
p = ps.ProximitySensor()

p.setHighThreshold(10000)
p.setInterrupt(1)


def sensorEvent(pin):
	s.ledDrv(1)
	s.setBank(3)
	r = s.readAllCal()
	s.ledDrv(0)
	print(r)
	servo.open()
	time.sleep(0.1)
	servo.close()
	GPIO.remove_event_detect(17)
	p.resetInterrupt()
	GPIO.add_event_detect(17,GPIO.FALLING,callback=sensorEvent)

interruptPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(interruptPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17,GPIO.FALLING,callback=sensorEvent)



count = 0
while(True):
	try:
		count = count + 1
		print("Doing Other Stuff " + str(count))
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