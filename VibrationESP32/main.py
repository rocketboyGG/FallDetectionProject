from machine import Pin
from lib.battery_status import BatteryStatus
from lib.mqtt import MQTT
from time import sleep, time

motor = Pin(23, Pin.OUT)
battery = BatteryStatus(35)
mqtt = MQTT()

def on_message(topic, msg):
    global motor
    print((topic, msg))
    if msg == b"Activate":
        motor.value(1)
        sleep(5)
        motor.value(0)

mqtt.client.set_callback(on_message)
mqtt.client.subscribe(b"vibration/activate")

last_batt_send = time()

while True:
    mqtt.client.check_msg()
    now = time()
    if now - last_batt_send >= 60:
        batt = battery.getPercentage_batt()
        #print("Sending battery:", batt)
        mqtt.client.publish(b"vibration/battery", str(batt))
        last_batt_send = now
    sleep(1)

