import network, ubinascii
from umqtt.simple import MQTTClient
from time import sleep

class MQTT:
    def __init__(self):
        ssid = "The Beast"
        password = "w2u8kdze"
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        self.wifi.connect(ssid, password)
        while not self.wifi.isconnected():
            sleep(0.5)
        print("Connected to Wi-Fi")

        # MQTT broker info
        mqtt_server = "10.19.144.9"
        client_id = self.get_unique_id()

        # Connect til MQTT broker
        self.client = MQTTClient(client_id, mqtt_server)
        self.client.connect()
        print("Connected to MQTT broker")

    def get_unique_id(self):
        # Get the MAC address of the device
        wlan = network.WLAN(network.STA_IF)
        mac = ubinascii.hexlify(wlan.config('mac'), ':').decode()
        # Use the MAC address to create a unique Client ID
        return b'esp32_' + ubinascii.hexlify(wlan.config('mac'))
