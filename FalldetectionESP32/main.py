from machine import I2C, Pin
from lib.imu_sensor import IMU
from lib.battery_status import BatteryStatus
from lib.button import Button
from lib.SignalLightTest import SignalLight
from lib.heart_rate import HeartRateSensor
from lib.mqtt import MQTT
from time import sleep, time

i2c = I2C(scl=Pin(22), sda=Pin(21))
heart_rate_sensor = HeartRateSensor(i2c)
imu_sensor = IMU(i2c)
but = Button(35) 
fallLight = SignalLight(18)
possibleLight = SignalLight(19)
buttonLight = SignalLight(32)
battery_status = BatteryStatus(34)
mqtt = MQTT()

mqtt_lasttime1 = time()
mqtt_lasttime2 = time()

while True:
    heart_rate_sensor.run_sensor()
    status = imu_sensor.calculateSpike()
    button_status = but.manuelActivationCheck()
    if status[1] or button_status:
        print("FALL PUBLISHED VIA MQTT")
        mqtt.client.publish(b"fallband/fall", "FALL")

    possibleLight.light(status[0])
    fallLight.light(status[1])
    buttonLight.light(button_status)

    if time() - mqtt_lasttime1 >= 10:
        print("Publish heart_rate status:", heart_rate_sensor.current_heart_rate)
        mqtt.client.publish(b"fallband/pulse", str(heart_rate_sensor.current_heart_rate))
        mqtt_lasttime1 = time()
    
    if time() - mqtt_lasttime2 >= 6:
        bat = battery_status.getPercentage_batt()
        print("Publish battery status:", bat)
        mqtt.client.publish(b"fallband/battery", str(bat))
        mqtt_lasttime2 = time() 

    