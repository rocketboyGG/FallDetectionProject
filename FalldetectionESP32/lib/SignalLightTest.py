from machine import Pin
from time import ticks_ms

class SignalLight:
    def __init__(self, pin_num):
        self.led = Pin(pin_num, Pin.OUT)
        self.led_start = True
        self.lastime = 0
    
    def light(self, enabled):
        if enabled:
            if self.led_start:
                self.led.value(1)
                self.led_start = False
                self.lastime = ticks_ms()
        if not self.led_start:
            if ticks_ms() - self.lastime >= 1000:
                self.led.value(0)
                self.led_start = True

        

