import smbus
from I2C_prox import write,read
import time
import math
import numpy as np
import bitstring as bs



class ProximitySensor:
	def __init__(self):
		self.bus = smbus.SMBus(1)
		self.setLedLevel(20)

	def getProximity(self):
		write(self.bus,0x80,0x08)
		while(not (read(self.bus,0x80)&0x20)):
			pass
		h = read(self.bus,0x87)
		d = h << 8 | read(self.bus,0x88)
		return d

	def setLedLevel(self,lvl:int):
		if(lvl >=0 and lvl <= 20):
			write(self.bus,0x83,lvl)

	def setInterrupt(self,state=0):
		if(state):
			write(self.bus,0x80,0x03)
			write(self.bus,0x89,2)	# Enable interrupt 
		else:
			write(self.bus,0x80,0x00)
			write(self.bus,0x89,0)  # Disable interrupt 

	def getInterruptStatus(self):
		return read(self.bus,0x8E)

	def resetInterrupt(self):
		write(self.bus,0x8E,0x02)
		
	def setLowThreshold(self,t):
		highBits = (0xFF00 & t) >> 8
		lowBits  = (0x00FF & t)
		write(self.bus,0x8A,highBits)	# Enable interrupt 
		write(self.bus,0x8B,lowBits)	# Enable interrupt 

	def setHighThreshold(self,t):	
		highBits = (0xFF00 & t) >> 8
		lowBits  = (0x00FF & t)
		write(self.bus,0x8C,highBits)	# Enable interrupt 
		write(self.bus,0x8D,lowBits)	# Enable interrupt 

	def getLowThreshold(self):
		highBits = read(self.bus,0x8A)	
		lowBits  = read(self.bus,0x8B)
		return (highBits << 8) | lowBits	 

	def getHighThreshold(self):
		highBits = read(self.bus,0x8C)	
		lowBits  = read(self.bus,0x8D)
		return (highBits << 8) | lowBits	







