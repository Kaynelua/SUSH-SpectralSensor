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

	def setBank(self,bank:int):
		reg = read(self.bus,0x04)
		reg = reg & 0xF3
		write(self.bus,0x04, reg|bank<<2)

	def dataReady(self):
		reg = read(self.bus,0x04)
		return bool(reg & 0x02)

	def readChan(self,chan):
		while( not self.dataReady()):
			pass
		if(chan=='V'):
			hi = read(self.bus,0x08)
			lo = read(self.bus,0x09)
			return (hi << 8 | lo)
