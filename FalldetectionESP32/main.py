from machine import I2C, Pin
from lib.imu_sensor import IMU
from lib.battery_status import BatteryStatus
from lib.lmt87 import LMT87
from lib.button import Button
from SignalLightTest import SignalLight
from time import sleep

imu_sensor = IMU()
lmt = LMT87(33)
but = Button()
fallLight = SignalLight(25)
possibleLight = SignalLight(26)
buttonLight = SignalLight(32)
battery_status = BatteryStatus()

while True:
    status = imu_sensor.calculateSpike()
    button_status = but.manuelActivationCheck()
    
    possibleLight.light(status[0])
    fallLight.light(status[1])
    buttonLight.light(button_status)
    
    #print(battery_status.getPercentage_batt())   
    #print("IMU temp ", imu_sensor.imu.get_values().get("temperature celsius"))
    #print("LMT87 temp ", lmt.get_temperature())
    #sleep(1)
    

