#!/usr/bin/env python 

from smbus import SMBus
  
DEVICE_ADDRESS = 0x18	# Starting I2C address

# Register configuration
INPUT_REG_ADDR          = 0x00
OUTPUT_REG_ADDR         = 0x01
POLARITY_REG_REG_ADDR   = 0x02
CONFIG_REG_ADDR         = 0x03

RELAYs_ON_BOARD = 0xF1	# 3 Relay available 

ALL_RELAY_ON	= 0x0E
ALL_RELAY_OFF	= 0x00

bus = SMBus(1)

def i2c_check(addr):
	config = bus.read_byte_data(addr, CONFIG_REG_ADDR)
	if config:
		bus.write_byte_data(addr, CONFIG_REG_ADDR, RELAYs_ON_BOARD)
	return bus.read_byte_data(addr, INPUT_REG_ADDR)

def set_zrelay_state(stack_level , relay_num , state):
	relay_num = relay_num + 1
	if stack_level < 0 or stack_level > 7:
		raise ValueError('Invalid stack level')
		return

	if relay_num < 2 or relay_num > 4:
		raise ValueError('Invalid relay number')
		return

	read_val = i2c_check(DEVICE_ADDRESS + stack_level)
	
	if state == 1:
		val = read_val | (1 << (relay_num - 1))
		bus.write_byte_data(DEVICE_ADDRESS + stack_level, OUTPUT_REG_ADDR, val)
	
	if state == 0:
		val = read_val & (~(1 << (relay_num - 1)))
		bus.write_byte_data(DEVICE_ADDRESS + stack_level, OUTPUT_REG_ADDR, val)


def set_all_zrelay_state(stack_level, state):
	if stack_level < 0 or stack_level > 7:
		raise ValueError('Invalid stack level')
		return

	i2c_check(DEVICE_ADDRESS  + stack_level)	
	if state == 1:
		bus.write_byte_data(DEVICE_ADDRESS + stack_level, OUTPUT_REG_ADDR, ALL_RELAY_ON)

	if state == 0:
		bus.write_byte_data(DEVICE_ADDRESS + stack_level, OUTPUT_REG_ADDR, ALL_RELAY_OFF)


def get_zrelay_state(stack_level, relay_num):
	relay_num = relay_num + 1
	if stack_level < 0 or stack_level > 7:
		raise ValueError('Invalid stack level')
		return
	
	if relay_num < 2 or relay_num > 4:
		raise ValueError('Invalid relay number')
		return
	
	i2c_check(DEVICE_ADDRESS + stack_level)
	read_val = bus.read_byte_data(DEVICE_ADDRESS + stack_level, INPUT_REG_ADDR)
	val = read_val & (1 << (relay_num - 1))
	if val:
		return 1 # Realay ON
	else:
		return 0 # Realay OFF

def get_all_zrelay_state(stack_level):
	if stack_level < 0 or stack_level > 7:
		raise ValueError('Invalid stack level')
		return

	val = i2c_check(DEVICE_ADDRESS + stack_level)
	return val
