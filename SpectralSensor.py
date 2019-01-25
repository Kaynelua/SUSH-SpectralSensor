import smbus
from I2C import write,read

class SpectralSensor:
	def __init__(self):
		self.bus = smbus.SMBus(1)

	def ledInd(self,state:bool):
		reg = read(self.bus,0x07)
		if(state):
			write(self.bus,0x07,reg | 0x01)
		else:
			write(self.bus,0x07,reg & 0xFE)
	def reset(self):
		reg = read(self.bus,0x04)
		write(self.bus,0x04,reg|0x80) 
