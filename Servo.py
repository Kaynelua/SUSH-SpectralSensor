import RPi.GPIO as GPIO
import time

pwmPin = 18
GPIO.setmode(GPIO.BCM) 
GPIO.setup(pwmPin,GPIO.OUT)
servo = GPIO.PWM(18,50)

def open():				#Turn servo 90degrees to open gate for plate to be flushed out
	servo.start(10)
	time.sleep(0.5)
	servo.ChangeDutyCycle(0)
def close():			#Turn servo back 90 degrees to close gate to block next plate from dropping out
	servo.start(5)
	time.sleep(0.5)
	servo.ChangeDutyCycle(0)
