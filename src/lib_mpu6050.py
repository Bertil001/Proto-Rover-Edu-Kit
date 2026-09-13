# lib_mpu6050.py - Driver basique
import machine

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00') # Réveil du capteur

    def get_accel(self):
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 6)
        # Conversion des octets bruts en valeurs lisibles
        x = (data[0] << 8 | data[1])
        y = (data[2] << 8 | data[3])
        z = (data[4] << 8 | data[5])
        return x, y, z