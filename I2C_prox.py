import smbus

def write(bus, vaddr:int, val:int):
	bus.write_byte_data(0x13,vaddr, val) 		# send data to buffer

def read(bus, vaddr:int,):
	bus.write_byte_data(0x13,vaddr,0x00)		# send vaddr to buffer
	return bus.read_byte_data(0x13,vaddr) 		# read data from buffer
