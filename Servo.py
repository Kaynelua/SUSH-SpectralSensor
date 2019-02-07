import RPi.GPIO as GPIO
import time

pwmPin = 18
GPIO.setmode(GPIO.BCM) 
GPIO.setup(pwmPin,GPIO.OUT)
servo = GPIO.PWM(18,50)

def open():
	servo.start(10)
	time.sleep(0.5)
	servo.ChangeDutyCycle(0)
def close():
	servo.start(5)
	time.sleep(0.5)
	servo.ChangeDutyCycle(0)
