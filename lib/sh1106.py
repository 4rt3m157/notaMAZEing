# Minimal SH1106 128x64 OLED driver for MicroPython (I2C).
# Subclasses framebuf.FrameBuffer so the user can call any framebuf method
# (text, pixel, line, rect, fill, blit, ...) then push with .show().

import framebuf
from micropython import const

_SET_CONTRAST        = const(0x81)
_SET_ENTIRE_ON       = const(0xA4)
_SET_NORM_INV        = const(0xA6)
_SET_DISP            = const(0xAE)
_SET_MEM_ADDR        = const(0x20)
_SET_COL_LO          = const(0x00)
_SET_COL_HI          = const(0x10)
_SET_DISP_START_LINE = const(0x40)
_SET_SEG_REMAP       = const(0xA0)
_SET_MUX_RATIO       = const(0xA8)
_SET_COM_OUT_DIR     = const(0xC0)
_SET_DISP_OFFSET     = const(0xD3)
_SET_COM_PIN_CFG     = const(0xDA)
_SET_DISP_CLK_DIV    = const(0xD5)
_SET_PRECHARGE       = const(0xD9)
_SET_VCOM_DESEL      = const(0xDB)
_SET_CHARGE_PUMP     = const(0xAD)
_SET_PAGE_ADDR       = const(0xB0)


class SH1106_I2C(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.pages = height // 8
        # SH1106 has 132 columns; visible window starts at column 2.
        self._col_offset = 2
        self.buffer = bytearray(self.pages * width)
        super().__init__(self.buffer, width, height, framebuf.MONO_VLSB)
        self._init_display()

    def _write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytes([0x80, cmd]))

    def _init_display(self):
        for cmd in (
            _SET_DISP | 0x00,
            _SET_DISP_CLK_DIV, 0x80,
            _SET_MUX_RATIO, self.height - 1,
            _SET_DISP_OFFSET, 0x00,
            _SET_DISP_START_LINE | 0x00,
            _SET_CHARGE_PUMP, 0x8B,
            _SET_SEG_REMAP | 0x01,
            _SET_COM_OUT_DIR | 0x08,
            _SET_COM_PIN_CFG, 0x12,
            _SET_CONTRAST, 0xFF,
            _SET_PRECHARGE, 0x1F,
            _SET_VCOM_DESEL, 0x40,
            _SET_ENTIRE_ON,
            _SET_NORM_INV,
            _SET_DISP | 0x01,
        ):
            self._write_cmd(cmd)
        self.fill(0)
        self.show()

    def contrast(self, value):
        self._write_cmd(_SET_CONTRAST)
        self._write_cmd(value & 0xFF)

    def invert(self, invert):
        self._write_cmd(_SET_NORM_INV | (1 if invert else 0))

    def poweron(self):
        self._write_cmd(_SET_DISP | 0x01)

    def poweroff(self):
        self._write_cmd(_SET_DISP | 0x00)

    def show(self):
        for page in range(self.pages):
            self._write_cmd(_SET_PAGE_ADDR | page)
            self._write_cmd(_SET_COL_LO | (self._col_offset & 0x0F))
            self._write_cmd(_SET_COL_HI | (self._col_offset >> 4))
            start = page * self.width
            # Co=0, D/C=1 → data stream
            self.i2c.writeto(self.addr, b"\x40" + self.buffer[start:start + self.width])
