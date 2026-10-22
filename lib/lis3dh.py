# Minimal LIS3DH 3-axis accelerometer driver (I2C, ±2g, 100Hz).
# Returns floats in "g" (1.0 ≈ 1g).

from micropython import const
import struct

_WHO_AM_I  = const(0x0F)
_CTRL_REG1 = const(0x20)
_CTRL_REG4 = const(0x23)
_OUT_X_L   = const(0x28)
_AUTO_INC  = const(0x80)


class LIS3DH:
    def __init__(self, i2c, addr=0x19):
        self.i2c = i2c
        self.addr = addr
        who = self.i2c.readfrom_mem(self.addr, _WHO_AM_I, 1)[0]
        if who != 0x33:
            raise OSError("LIS3DH not found (WHO_AM_I=0x%02X)" % who)
        # 100 Hz, normal mode, all axes enabled
        self.i2c.writeto_mem(self.addr, _CTRL_REG1, bytes([0x57]))
        # ±2g, high-resolution disabled (normal mode → 10-bit data)
        self.i2c.writeto_mem(self.addr, _CTRL_REG4, bytes([0x00]))

    def read_raw(self):
        # Auto-increment to read 6 bytes in one transaction.
        raw = self.i2c.readfrom_mem(self.addr, _OUT_X_L | _AUTO_INC, 6)
        x, y, z = struct.unpack("<hhh", raw)
        return x, y, z

    def read_g(self):
        # Normal mode @ ±2g: full scale = 16384 LSB/g (shift by 6 for 10-bit).
        x, y, z = self.read_raw()
        scale = 1.0 / 16384.0
        return (x * scale, y * scale, z * scale)
