import smbus

def write(bus, vaddr:int, val:int):
	while(bus.read_byte_data(0x13,0x00) & 0x02):		# check tx_valid bit
		pass
	bus.write_byte_data(0x49,0x01,0x80 | vaddr)	# send vaddr to buffer
	while(bus.read_byte_data(0x13,0x00) & 0x02):		# check tx_valid bit
		pass
	bus.write_byte_data(0x13,0x01, val) 		# send data to buffer

def read(bus, vaddr:int,):
	bus.write_byte_data(0x13,0x81,0x00)		# send vaddr to buffer
	return bus.read_byte_data(0x13,0x81) 		# read data from buffer
