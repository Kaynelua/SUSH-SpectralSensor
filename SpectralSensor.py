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
	def ledDrv(self,level):
		reg = read(self.bus,0x07)
		if(level >0):
			reg = reg & 0xCF
			level = (level -1) << 4
			write(self.bus,0x07,reg|0x08|level)
		else :
			write(self.bus,0x07,reg& 0xF7)
	
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
		addr = {'V' : [0x08,0x09], 'B' : [0x0A,0x0B], 'G' : [0x0C,0x0D], 'Y' : [0x0E,0x0F], 'O' : [0x10,0x11], 'R' : [0x12,0x13] }
		hi = read(self.bus,addr[chan][0])
		lo = read(self.bus,addr[chan][1])
		return (hi << 8 | lo)
