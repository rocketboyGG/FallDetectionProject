from machine import I2C, Pin
from imu import MPU6050
from time import ticks_ms
from math import sqrt

class IMU:
    def __init__(self, i2c):
        self.imu = MPU6050(i2c)
        
        self.lasttime = 0
        self.lasttimeFallCheck = 0
        
        self.sampleInterval = 20
        self.fallThreshold_accel = 150
        self.fallThreshold_gyro = 15000
        
        self.stillThreshold_accel = 10
        self.stillThreshold_gyro = 500
        
        self.waittime_after_fall = 1000
        self.possibleFall = False
        self.fall = False
        self.waitCount = 0

        self.prev_accel = self.imu.accel.xyz
        self.prev_gyro = self.imu.gyro.xyz
        
    def getIMUData(self):
        try:
            return self.imu.get_values()
        except OSError:
            print("IMU FAILED!!!!!!!!!!!!")
            return {}
    
    def printIMUdata(self):
        print(self.imu.accel.xyz)
    
    def calculateSpike(self): 
        self.fall = False
        if (ticks_ms() - self.lasttime >= self.sampleInterval):
            jerk_x = (self.imu.accel.x - self.prev_accel[0]) / (self.sampleInterval / 1000)
            jerk_y = (self.imu.accel.y - self.prev_accel[1]) / (self.sampleInterval / 1000)
            jerk_z = (self.imu.accel.z - self.prev_accel[2]) / (self.sampleInterval / 1000)
            
            jerk_gyro_x = (self.imu.gyro.x - self.prev_gyro[0]) / (self.sampleInterval / 1000)
            jerk_gyro_y = (self.imu.gyro.y - self.prev_gyro[1]) / (self.sampleInterval / 1000)
            jerk_gyro_z = (self.imu.gyro.z - self.prev_gyro[2]) / (self.sampleInterval / 1000)
            
            self.prev_accel = self.imu.accel.xyz
            self.prev_gyro = self.imu.gyro.xyz
            
            magnitude_accel = sqrt(jerk_x**2 + jerk_y**2 + jerk_z**2)
            magnitude_gyro = sqrt(jerk_gyro_x**2 + jerk_gyro_y**2 + jerk_gyro_z**2)
            
            #print(magnitude_accel, magnitude_gyro)
            if (not self.possibleFall):
                if (magnitude_accel > self.fallThreshold_accel or magnitude_gyro > self.fallThreshold_gyro):
                    self.possibleFall = True
                    self.lasttimeFallCheck = ticks_ms()
            else:
                if (ticks_ms() - self.lasttimeFallCheck > self.waittime_after_fall):
                    if (magnitude_accel > self.stillThreshold_accel and magnitude_gyro > self.stillThreshold_gyro):
                        self.possibleFall = False
                        self.waitCount = 0
                    else:
                        #print("adding to waitcount", self.waitCount)
                        self.waitCount += 1
                        if self.waitCount >= 250:
                            self.fall = True
                            self.possibleFall = False
                            self.waitCount = 0
                            print("!!!!!FALL DETECTED!!!!!")
            
            self.lasttime = ticks_ms()
        return (self.possibleFall, self.fall)

    def printIMUData(self):
        imu_data = self.getIMUData()
        print("Accel x: " + str(imu_data.get("acceleration x")) + " Accel y: " + str(imu_data.get("acceleration y")) + " Accel z: "+str(imu_data.get("acceleration z"))  )
        


