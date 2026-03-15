import board
import time
import microcontroller
import neopixel
import math
import adafruit_qmc5883p

# CREATE MAGNETOMETER
i2c = board.STEMMA_I2C()
sensor = adafruit_qmc5883p.QMC5883P(i2c)

while True:
    time.sleep(0.125)
    mag_x, mag_y, mag_z = sensor.magnetic
#     print("X: {:.2f} uT, Y: {:.2f} uT, Z: {:.2f} uT".format(mag_x, mag_y, mag_z))
    
    heading = math.atan2(mag_y, mag_x)
    if heading < 0:
        heading += 2 * math.pi
 