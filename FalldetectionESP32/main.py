import network
from umqtt.simple import MQTTClient
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

# Tilslut Wi-Fi
ssid = "The Beast"
password = "w2u8kdze"
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
while not wifi.isconnected():
    time.sleep(0.5)
print("Connected to Wi-Fi")

# MQTT broker info
mqtt_server = "10.19.144.9"
client_id = "esp32_client"

# Connect til MQTT broker
client = MQTTClient(client_id, mqtt_server)
client.connect()
print("Connected to MQTT broker")

while True:
    status = imu_sensor.calculateSpike()
    if status[1] == True:
        client.publish(b"esp32/fall", "FALL")
    button_status = but.manuelActivationCheck()

    
    possibleLight.light(status[0])
    fallLight.light(status[1])
    buttonLight.light(button_status)
    
    #print(battery_status.getPercentage_batt())   
    #print("IMU temp ", imu_sensor.imu.get_values().get("temperature celsius"))
    #print("LMT87 temp ", lmt.get_temperature())
    #sleep(1)
    

