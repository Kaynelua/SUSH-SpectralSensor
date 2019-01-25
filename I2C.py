import smbus


# write_i2c_block_data(int addr,char cmd,long vals[])
# long[] read_i2c_block_data(int addr,char cmd)

# long read_byte_data(int addr,char cmd)
# long write_byte_data(int addr,char cmd,char val)


def write(bus, vaddr:int, val:int):
	while(bus.read_byte(0x49,0x00) & 0x02):		# check tx_valid bit
		pass
	bus.write_byte_data(0x49,0x01,0x80 | vaddr)	# send vaddr to buffer
	while(bus.read_byte(0x49,0x00) & 0x02):		# check tx_valid bit
		pass
	bus.write_byte_data(0x49,0x01, val) 		# send data to buffer

def read(bus, vaddr:int,):
	while(bus.read_byte(0x49,0x00) & 0x02):		# check tx_valid bit
		pass
	bus.write_byte_data(0x49,0x01, vaddr)		# send vaddr to buffer
	while(!bus.read_byte(0x49,0x00) & 0x01):		# check rx_valid bit
		pass
	bus.write_read_data(0x49,0x02, val) 		# read data from buffer

