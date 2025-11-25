from machine import I2C, Pin
from lib.imu_sensor import IMU
from time import sleep

i2c = I2C(scl=Pin(22), sda=Pin(21))
imu_sensor = IMU(i2c)

while True:
    imu_sensor.calculateSpike()
