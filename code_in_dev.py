import board
import time
import microcontroller
import neopixel
import math

# CREATE RADIOSHACK ACCESS POINT
import radioshack_create_access_point
import radioshack_create_www_websocket
# QMC588L MAGNETOMETER
import adafruit_qmc5883p
# MOTOR DRIVER
from radioshack_motors import *

# CREATE MAGNETOMETER
i2c = board.STEMMA_I2C()
sensor = adafruit_qmc5883p.QMC5883P(i2c)

def cardinal():
	time.sleep(0.125)
	mag_x, mag_y, mag_z = sensor.magnetic
	# print("X: {:.2f} uT, Y: {:.2f} uT, Z: {:.2f} uT".format(mag_x, mag_y, mag_z))
	
	heading = math.atan2(mag_y, mag_x)
	if heading < 0:
		heading += 2 * math.pi
		
	print("Heading: {:.2f} degrees".format(math.degrees(heading) - 15))


while True:
	cardinal()
	pass