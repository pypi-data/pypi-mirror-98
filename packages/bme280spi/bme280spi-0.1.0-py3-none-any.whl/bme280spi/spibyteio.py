# Copyright (c) 2021
# Author: Kuzj  # noqa E800
# Based on I2C.py created by Tony DiCola
# Based on Adafruit_I2C.py created by Kevin Townsend.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import spidev

from typing import List

WRITE = 0x7F
SPEED_HZ = 500000


class Device(object):
    """Spidev device with byte communucation."""

    def __init__(
        self,
        bus: int,
        dev: int,
        speed_hz: int = SPEED_HZ,
        delay_usec: int = 0,
        xfer: int = 1,
    ):
        """Device initialization."""
        assert xfer in [1, 2, 3]
        self._dev = spidev.SpiDev()
        self._dev.open(bus, dev)
        self._speed_hz = speed_hz
        self._delay_usec = delay_usec
        if xfer == 1:
            self._xfer = self._dev.xfer
        elif xfer == 2:
            self._xfer = self._dev.xfer2
        else:
            self._xfer = self._dev.xfer3
        self._logger = logging.getLogger('Spi.Device.Bus.{0}.Dev.{1}'.format(bus, dev))

    def write8(self, register: int, value: int):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        to_send = [register & WRITE, value]
        self._xfer(to_send, self._speed_hz, self._delay_usec)
        self._logger.debug(
            'Wrote 0x{0:02X} to register 0x{1:02X}'.format(value, register)
        )

    def write16(self, register: int, value: int):
        """Write a 16-bit value to the specified register."""
        value = value & 0xFFFF
        to_send = [register & WRITE, value >> 8, value & 0xFF]
        self._xfer(to_send, self._speed_hz, self._delay_usec)
        self._logger.debug(
            'Wrote 0x{0:04X} to register pair 0x{1:02X}, 0x{2:02X}'.format(
                value,
                register,
                register + 1,
            )
        )

    def writeList(self, register: int, data: List[int]):
        """Write bytes to the specified register."""
        to_send = [register & WRITE] + data
        self._xfer(to_send, self._speed_hz, self._delay_usec)
        self._logger.debug('Wrote to register 0x{0:02X}: {1}'.format(register, data))

    def readList(self, register: int, length: int):
        """Read a length number of bytes from the specified register. Results
        will be returned as a bytearray.
        """
        to_send = [register] + [0] * length
        result = self._xfer(to_send, self._speed_hz, self._delay_usec)[1:]
        self._logger.debug(
            'Read the following from register 0x{0:02X}: {1}'.format(register, result)
        )
        return result

    def readU8(self, register: int):
        """Read an unsigned byte from the specified register."""
        to_send = [register, 0]
        result = self._xfer(to_send, self._speed_hz, self._delay_usec)[1]
        self._logger.debug(
            'Read 0x{0:02X} from register 0x{1:02X}'.format(result, register)
        )
        return result

    def readS8(self, register: int):
        """Read a signed byte from the specified register."""
        result = self.readU8(register)
        if result > 127:
            result -= 256
        return result

    def readU16(self, register: int, little_endian: bool = True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        to_send = [register, 0, 0]
        reg, d1, d2 = self._xfer(to_send, self._speed_hz, self._delay_usec)
        result = (d1 << 8) + d2
        self._logger.debug(
            'Read 0x{0:04X} from register pair 0x{1:02X}, 0x{2:02X}'.format(
                result,
                register,
                register + 1,
            )
        )
        # Swap bytes if using big endian because read_word_data assumes little
        # endian on ARM (little endian) systems.
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result

    def readS16(self, register: int, little_endian: bool = True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        result = self.readU16(register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def readU16LE(self, register: int):
        """Read an unsigned 16-bit value from the specified register, in little
        endian byte order.
        """
        return self.readU16(register, little_endian=True)

    def readU16BE(self, register: int):
        """Read an unsigned 16-bit value from the specified register, in big
        endian byte order.
        """
        return self.readU16(register, little_endian=False)

    def readS16LE(self, register: int):
        """Read a signed 16-bit value from the specified register, in little
        endian byte order.
        """
        return self.readS16(register, little_endian=True)

    def readS16BE(self, register: int):
        """Read a signed 16-bit value from the specified register, in big
        endian byte order.
        """
        return self.readS16(register, little_endian=False)
