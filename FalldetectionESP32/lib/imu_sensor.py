from machine import I2C, Pin
from mpu6050 import MPU6050
from time import ticks_ms
from math import sqrt

class IMU:
    def __init__(self, i2c):
        self.imu = MPU6050(i2c)
        self.lasttime = 0
        self.lasttimeFallCheck = 0
        self.sampleInterval = 200
        self.fallThreshold = 10000
        self.stillThreshold = 1000
        self.possibleFall = False
        self.waitCount = 0
        self.firstFallCheck = False
        
        imu_data = self.imu.get_values()
        self.prev_g_x = imu_data.get("acceleration x") / 9.8
        self.prev_g_y = imu_data.get("acceleration y") / 9.8
        self.prev_g_z = imu_data.get("acceleration z") / 9.8
        
    def getIMUData(self):
        try:
            return self.imu.get_values()
        except OSError:
            print("IMU FAILED!!!!!!!!!!!!")
            return {}
    
    def calculateSpike(self):
        
        if (ticks_ms() - self.lasttime >= self.sampleInterval):
            self.lasttime = ticks_ms()
            imu_data = self.getIMUData()
            
            g_x = imu_data.get("acceleration x") / 9.8
            g_y = imu_data.get("acceleration y") / 9.8
            g_z = imu_data.get("acceleration z") / 9.8
            
            jerk_x = (g_x - self.prev_g_x) / (self.sampleInterval / 1000)
            jerk_y = (g_y - self.prev_g_y) / (self.sampleInterval / 1000)
            jerk_z = (g_z - self.prev_g_z) / (self.sampleInterval / 1000)
            
            self.prev_g_x = g_x
            self.prev_g_y = g_y
            self.prev_g_z = g_z
            
            magnitude = sqrt(jerk_x * jerk_x + jerk_y * jerk_y + jerk_z * jerk_z)
            print(magnitude)
            if (not self.possibleFall):
                if (magnitude > self.fallThreshold):
                    print("POSSIBLE FALL DETECTED")
                    self.possibleFall = True
                    self.firstFallCheck = True
                    self.lasttimeFallCheck = ticks_ms()
            else:
                if (ticks_ms() - self.lasttimeFallCheck > 1000):
                    if (magnitude > self.stillThreshold):
                        self.possibleFall = False
                        self.waitCount = 0
                    else:
                        print("adding to waitcount", self.waitCount)
                        self.waitCount += 1
                        if self.waitCount >= 10:
                            print("!!!!!FALL DETECTED!!!!!")
                

    def printIMUData(self):
        imu_data = self.getIMUData()
        print("Accel x: " + str(imu_data.get("acceleration x")) + " Accel y: " + str(imu_data.get("acceleration y")) + " Accel z: "+str(imu_data.get("acceleration z"))  )
        


