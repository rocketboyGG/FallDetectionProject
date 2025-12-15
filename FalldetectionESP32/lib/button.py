from machine import Pin
from time import ticks_ms

class Button:
    def __init__(self, pin_num):
        self.but = Pin(pin_num, Pin.IN)
        self.lasttime = ticks_ms()
        self.waitcount = 0
        
    def manuelActivationCheck(self):
        if ticks_ms() - self.lasttime > 1000:
            if self.but.value() == 1:
                self.waitcount += 1
                if self.waitcount >= 5:
                    self.waitcount = 0
                    return True
                    print("MANUEL FALL DETECTION!!!!")
            else:
                self.waitcount = 0
            self.lasttime = ticks_ms()      
        return False
        
    def printStatus(self):
        print(self.but.value())