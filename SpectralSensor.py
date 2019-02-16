import smbus
from I2C import write,read
import time
import math
import numpy as np
import bitstring as bs

class SpectralSensor:
	def __init__(self):
		self.bus = smbus.SMBus(1)
		self.gain(2)

	def gain(self,level): #Set sensor gain
		if(level >=0 and level <=3):
			reg = read(self.bus,0x07)
			reg = reg & 0xCF
			write(self.bus,0x07,reg|level<<4)

	def ledInd(self,state:bool): #Turn on LED indicator light
		reg = read(self.bus,0x07)
		if(state):
			write(self.bus,0x07,reg | 0x01)
		else:
			write(self.bus,0x07,reg & 0xFE)

	def ledDrv(self,level): #Turn on Driver LED light
		reg = read(self.bus,0x07)
		if(level == 1):
			reg = reg & 0xCF
			level = (level -1) << 4
			write(self.bus,0x07,reg|0x08|level)
		else :
			write(self.bus,0x07,reg& 0xF7)
	
	def reset(self): #Resets sensor
		reg = read(self.bus,0x04)
		write(self.bus,0x04,reg|0x80) 

	def setBank(self,bank:int): #Sets bank to vary reading mode i.e one shot or continuous reading
		reg = read(self.bus,0x04)
		reg = reg & 0xF1
		write(self.bus,0x04, reg|bank<<2)

	def dataReady(self):	#Check if data is ready in the register
		reg = read(self.bus,0x04)
		return bool(reg & 0x02)

	def readChan(self,chan):	#For reading of raw values from a specific channel i.e intensity at particular frequency.
	#	while( not self.dataReady()):
	#		time.sleep(0.01)
			#pass
		addr = {'V' : [0x08,0x09], 'B' : [0x0A,0x0B], 'G' : [0x0C,0x0D], 'Y' : [0x0E,0x0F], 'O' : [0x10,0x11], 'R' : [0x12,0x13] }
		hi = read(self.bus,addr[chan][0])
		lo = read(self.bus,addr[chan][1])
		return (hi << 8 | lo)
	
	def readAll(self): #reads raw values from all 6 channels.
		colors =['V','B','G','Y','O','R']
		listSpectrum=[]
		for color in colors :
			val = self.readChan(color)
			listSpectrum.append(val)
		return listSpectrum
	
	def readAllCal(self): #reads calibrated readings from all 6 channels
		colors_add =[(0x14,0x15,0x16,0x17),(0x18,0x19,0x1A,0x1B),
(0x1C,0x1D,0x1E,0x1F),(0x20,0x21,0x22,0x23),(0x24,0x25,0x26,0x27),(0x28,0x29,0x2A,0x2B)]
		calSpectrum=[]
		while(not self.dataReady()):
			time.sleep(0.01)
		for color in colors_add :
			b3 = read(self.bus,color[0])
			b2 = read(self.bus,color[1])
			b1 = read(self.bus,color[2])
			b0 = read(self.bus,color[3])
			val = (b3<<24) | (b2<<16) | (b1<<8) |b0
			bin_val = np.binary_repr(val,width = 32)
			c = bs.BitArray(bin=bin_val)
			calSpectrum.append(c.float)
		return np.array(calSpectrum)
