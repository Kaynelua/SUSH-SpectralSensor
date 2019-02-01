import smbus
from I2C_prox import write,read
import time
import math
import numpy as np
import bitstring as bs



class ProximitySensor:
	def __init__(self):
		self.bus = smbus.SMBus(1)
		self.ledLevel(20)

	def readProximity(self):
		prox.write(bus,0x80,0x08)
        while(not (prox.read(bus,0x80)&0x20)):
                pass
        h = prox.read(bus,0x87)
        d = h << 8 | prox.read(bus,0x88)

    def ledLevel(self,lvl:int):
    	if(lvl >=0 and lvl <= 20):
    		prox.write(bus,0x83,lvl)