from machine import I2C, Pin
from lib.imu_sensor import IMU
from lib.battery_status import BatteryStatus
from time import sleep

i2c = I2C(scl=Pin(22), sda=Pin(21))
imu_sensor = IMU(i2c)

battery_status = BatteryStatus()

while True:
    #imu_sensor.calculateSpike()
    #print(battery_status.getPercentage_batt())
    
    print(imu_sensor.imu.get_values().get("temperature celsius"))
    sleep(0.5)
    

