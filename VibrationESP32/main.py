import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
from lib.battery_status import BatteryStatus
from time import sleep

# MQTT broker info
mqtt_server = "10.19.144.9"
client_id = "esp32_client"
topic_sub = b"led/control"

# Wi-Fi credentials
ssid = "The Beast"
password = "w2u8kdze"

# Tilslut Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    time.sleep(0.5)

print("Connected to Wi-Fi")

# Callback når besked modtages
def sub_cb(topic, msg):
    print((topic, msg))
    if msg == b"ON":
        motor.value(1)
        sleep(5)
        motor.value(0)

# Connect til MQTT broker
client = MQTTClient(client_id, mqtt_server)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)
print("Connected to MQTT broker, subscribed to topic")

# Motor til GPIO2
motor = Pin(23, Pin.OUT)
battery = BatteryStatus()

# Loop for at modtage beskeder og sende batteri-status
try:
    last_batt_send = time.time()
    SEND_INTERVAL = 1 * 10

    while True:
        # Handle incoming MQTT messages
        client.check_msg()
        
        # Check if it is time to send battery status
        now = time.time()
        if now - last_batt_send >= SEND_INTERVAL:
            batt = battery.getPercentage_batt()
            print("Sending battery:", batt)
            client.publish(b"esp32/battery", str(batt))
            last_batt_send = now

        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()


