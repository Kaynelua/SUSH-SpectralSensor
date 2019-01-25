import smbus
from I2C import write,read

class SpectralSensor:
	
	def __init__(self):
		self.bus = smbus.SMBus(1)

	def led_ind(state:bool):
		reg = read(self.bus,0x07)
		if(state):
			write(self.bus,reg & 0x0F)
		else:
			write(self.bus,reg & 0x0E)