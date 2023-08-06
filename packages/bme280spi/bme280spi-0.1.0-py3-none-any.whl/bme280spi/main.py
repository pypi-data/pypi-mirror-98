# Copyright (c) 2021
# Author: Kuzj  # noqa E800
#
# Based on the BMP280 driver created by Tony DiCola
# Based on the BMP280 driver with BME280 changes provided by
# David J Taylor, Edinburgh (www.satsignal.eu). Additional functions added
# by Tom Nardi (www.digifail.com)
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
import time
from collections import Counter

from bme280spi.spibyteio import Device
from bme280spi.helpers import round0, round01

BME280_CHIPID = 0x60

# Operating Modes
BME280_OSAMPLE_1 = 1
BME280_OSAMPLE_2 = 2
BME280_OSAMPLE_4 = 3
BME280_OSAMPLE_8 = 4
BME280_OSAMPLE_16 = 5

# Standby Settings
BME280_STANDBY_0p5 = 0
BME280_STANDBY_62p5 = 1
BME280_STANDBY_125 = 2
BME280_STANDBY_250 = 3
BME280_STANDBY_500 = 4
BME280_STANDBY_1000 = 5
BME280_STANDBY_10 = 6
BME280_STANDBY_20 = 7

# Filter Settings
BME280_FILTER_OFF = 0
BME280_FILTER_2 = 1
BME280_FILTER_4 = 2
BME280_FILTER_8 = 3
BME280_FILTER_16 = 4

# BME280 Registers

BME280_REGISTER_DIG_T1 = 0x88  # Trimming parameter registers
BME280_REGISTER_DIG_T2 = 0x8A
BME280_REGISTER_DIG_T3 = 0x8C

BME280_REGISTER_DIG_P1 = 0x8E
BME280_REGISTER_DIG_P2 = 0x90
BME280_REGISTER_DIG_P3 = 0x92
BME280_REGISTER_DIG_P4 = 0x94
BME280_REGISTER_DIG_P5 = 0x96
BME280_REGISTER_DIG_P6 = 0x98
BME280_REGISTER_DIG_P7 = 0x9A
BME280_REGISTER_DIG_P8 = 0x9C
BME280_REGISTER_DIG_P9 = 0x9E

BME280_REGISTER_DIG_H1 = 0xA1
BME280_REGISTER_DIG_H2 = 0xE1
BME280_REGISTER_DIG_H3 = 0xE3
BME280_REGISTER_DIG_H4 = 0xE4
BME280_REGISTER_DIG_H5 = 0xE5
BME280_REGISTER_DIG_H6 = 0xE6
BME280_REGISTER_DIG_H7 = 0xE7

BME280_REGISTER_CHIPID = 0xD0
BME280_REGISTER_VERSION = 0xD1
BME280_REGISTER_SOFTRESET = 0xE0

BME280_REGISTER_STATUS = 0xF3
BME280_REGISTER_CONTROL_HUM = 0xF2
BME280_REGISTER_CONTROL = 0xF4
BME280_REGISTER_CONFIG = 0xF5
BME280_REGISTER_DATA = 0xF7


class BME280ReadError(Exception):
    """Exception reading sensor data."""

    pass


_LOGGER = logging.getLogger(__name__)


class BME280(object):
    """Communication with Humidity sensor BME280."""

    def __init__(
        self,
        spi_bus: int = 0,
        spi_dev: int = 0,
        t_mode: int = BME280_OSAMPLE_1,
        p_mode: int = BME280_OSAMPLE_1,
        h_mode: int = BME280_OSAMPLE_1,
        standby: int = BME280_STANDBY_250,
        filter: int = BME280_FILTER_OFF,
        **kwargs,
    ):
        """Sensor initialization."""
        # Check that t_mode is valid.
        if t_mode not in [
            BME280_OSAMPLE_1,
            BME280_OSAMPLE_2,
            BME280_OSAMPLE_4,
            BME280_OSAMPLE_8,
            BME280_OSAMPLE_16,
        ]:
            raise ValueError('Unexpected t_mode value {0}.'.format(t_mode))
        self._t_mode = t_mode
        # Check that p_mode is valid.
        if p_mode not in [
            BME280_OSAMPLE_1,
            BME280_OSAMPLE_2,
            BME280_OSAMPLE_4,
            BME280_OSAMPLE_8,
            BME280_OSAMPLE_16,
        ]:
            raise ValueError('Unexpected p_mode value {0}.'.format(p_mode))
        self._p_mode = p_mode
        # Check that h_mode is valid.
        if h_mode not in [
            BME280_OSAMPLE_1,
            BME280_OSAMPLE_2,
            BME280_OSAMPLE_4,
            BME280_OSAMPLE_8,
            BME280_OSAMPLE_16,
        ]:
            raise ValueError('Unexpected h_mode value {0}.'.format(h_mode))
        self._h_mode = h_mode
        # Check that standby is valid.
        if standby not in [
            BME280_STANDBY_0p5,
            BME280_STANDBY_62p5,
            BME280_STANDBY_125,
            BME280_STANDBY_250,
            BME280_STANDBY_500,
            BME280_STANDBY_1000,
            BME280_STANDBY_10,
            BME280_STANDBY_20,
        ]:
            raise ValueError('Unexpected standby value {0}.'.format(standby))
        self._standby = standby
        # Check that filter is valid.
        if filter not in [
            BME280_FILTER_OFF,
            BME280_FILTER_2,
            BME280_FILTER_4,
            BME280_FILTER_8,
            BME280_FILTER_16,
        ]:
            raise ValueError('Unexpected filter value {0}.'.format(filter))
        self._filter = filter
        # Create SPI device.
        self._spi_bus = int(spi_bus)
        self._spi_dev = int(spi_dev)
        self._device = Device(self._spi_bus, self._spi_dev)
        # Check device ID.
        chip_id = self._device.readU8(BME280_REGISTER_CHIPID)
        if BME280_CHIPID != chip_id:
            raise RuntimeError('Failed to find BME280! Chip ID 0x{0:x}'.format(chip_id))
        # Load calibration values.
        self._load_calibration()
        self._device.write8(BME280_REGISTER_CONTROL, 0x24)  # Sleep mode
        time.sleep(0.002)
        self._device.write8(BME280_REGISTER_CONFIG, ((standby << 5) | (filter << 2)))
        time.sleep(0.002)
        self._device.write8(
            BME280_REGISTER_CONTROL_HUM, h_mode
        )  # Set Humidity Oversample
        self._device.write8(
            BME280_REGISTER_CONTROL, ((t_mode << 5) | (p_mode << 2) | 3)
        )  # Set Temp/Pressure Oversample and enter Normal mode(3) Forced mode(2)
        self._t_fine = 0.0
        self._humidity = 0.0
        self._temperature = 0.0
        self._pressure = 0
        self._ok = False
        self.update()

    def _load_calibration(self) -> None:

        self._dig_T1 = self._device.readU16BE(BME280_REGISTER_DIG_T1)
        self._dig_T2 = self._device.readS16BE(BME280_REGISTER_DIG_T2)
        self._dig_T3 = self._device.readS16BE(BME280_REGISTER_DIG_T3)

        self._dig_P1 = self._device.readU16BE(BME280_REGISTER_DIG_P1)
        self._dig_P2 = self._device.readS16BE(BME280_REGISTER_DIG_P2)
        self._dig_P3 = self._device.readS16BE(BME280_REGISTER_DIG_P3)
        self._dig_P4 = self._device.readS16BE(BME280_REGISTER_DIG_P4)
        self._dig_P5 = self._device.readS16BE(BME280_REGISTER_DIG_P5)
        self._dig_P6 = self._device.readS16BE(BME280_REGISTER_DIG_P6)
        self._dig_P7 = self._device.readS16BE(BME280_REGISTER_DIG_P7)
        self._dig_P8 = self._device.readS16BE(BME280_REGISTER_DIG_P8)
        self._dig_P9 = self._device.readS16BE(BME280_REGISTER_DIG_P9)

        self._dig_H1 = self._device.readU8(BME280_REGISTER_DIG_H1)
        self._dig_H2 = self._device.readS16BE(BME280_REGISTER_DIG_H2)
        self._dig_H3 = self._device.readU8(BME280_REGISTER_DIG_H3)
        self._dig_H6 = self._device.readS8(BME280_REGISTER_DIG_H7)

        h4 = self._device.readS8(BME280_REGISTER_DIG_H4)
        h4 = h4 << 4
        self._dig_H4 = h4 | (self._device.readU8(BME280_REGISTER_DIG_H5) & 0x0F)

        h5 = self._device.readS8(BME280_REGISTER_DIG_H6)
        h5 = h5 << 4
        self._dig_H5 = h5 | (self._device.readU8(BME280_REGISTER_DIG_H5) >> 4 & 0x0F)

    def _read_raw_temp(self) -> int:
        """Waits for reading to become available on device.
        Does a single burst read of all data values from device.
        Returns the raw (uncompensated) temperature from the sensor.
        """
        attempts = 0
        while self._device.readU8(BME280_REGISTER_STATUS) & 0x08:
            time.sleep(0.002)
            attempts += 1
            if attempts > 10:
                raise BME280ReadError('_read_raw_temp')
        self._BME280Data = self._device.readList(BME280_REGISTER_DATA, 8)
        raw = (
            (self._BME280Data[3] << 16)
            | (self._BME280Data[4] << 8)
            | self._BME280Data[5]
        ) >> 4
        return raw

    def _read_raw_temp2(self) -> int:
        """Reading while data don't repeat twice."""
        res_list = [[0]]
        while Counter(res_list).most_common(1)[0][1] < 2:
            self._read_raw_temp()
            res_list.append(list(self._BME280Data))
        _LOGGER.debug(f'spi{self._spi_bus}.{self._spi_dev}: {res_list}')
        self._BME280Data = Counter(res_list).most_common(1)[0][0]
        raw = (
            (self._BME280Data[3] << 16)
            | (self._BME280Data[4] << 8)
            | self._BME280Data[5]
        ) >> 4
        return raw

    def _read_raw_pressure(self) -> int:
        """Returns the raw (uncompensated) pressure level from the sensor.
        Assumes that the temperature has already been read
        i.e. that _BME280Data[] has been populated.
        """
        raw = (
            (self._BME280Data[0] << 16)
            | (self._BME280Data[1] << 8)
            | self._BME280Data[2]
        ) >> 4
        return raw

    def _read_raw_humidity(self) -> int:
        """Returns the raw (uncompensated) humidity value from the sensor.
        Assumes that the temperature has already been read
        i.e. that _BME280Data[] has been populated.
        """
        raw = (self._BME280Data[6] << 8) | self._BME280Data[7]
        return raw

    @round01
    def read_temperature(self) -> float:
        """Gets the compensated temperature in degrees celsius."""
        # float in Python is double precision
        ut = float(self._read_raw_temp())
        var1 = (ut / 16384.0 - float(self._dig_T1) / 1024.0) * float(self._dig_T2)
        var2 = (
            (ut / 131072.0 - float(self._dig_T1) / 8192.0)
            * (ut / 131072.0 - float(self._dig_T1) / 8192.0)
        ) * float(self._dig_T3)
        self._t_fine = int(var1 + var2)
        temp = (var1 + var2) / 5120.0
        return temp

    @round0
    def read_pressure(self) -> float:
        """Gets the compensated pressure in hPa."""
        adc = float(self._read_raw_pressure())
        var1 = float(self._t_fine) / 2.0 - 64000.0
        var2 = var1 * var1 * float(self._dig_P6) / 32768.0
        var2 = var2 + var1 * float(self._dig_P5) * 2.0
        var2 = var2 / 4.0 + float(self._dig_P4) * 65536.0
        var1 = (
            float(self._dig_P3) * var1 * var1 / 524288.0 + float(self._dig_P2) * var1
        ) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * float(self._dig_P1)
        if var1 == 0:
            return 0
        p = 1048576.0 - adc
        p = ((p - var2 / 4096.0) * 6250.0) / var1
        var1 = float(self._dig_P9) * p * p / 2147483648.0
        var2 = p * float(self._dig_P8) / 32768.0
        p = (p + (var1 + var2 + float(self._dig_P7)) / 16.0) / 100
        return p

    @round01
    def read_humidity(self) -> float:
        """Gets the compensated humidity."""
        adc = float(self._read_raw_humidity())
        h = float(self._t_fine) - 76800.0
        h = (adc - (float(self._dig_H4) * 64.0 + float(self._dig_H5) / 16384.0 * h)) * (
            float(self._dig_H2)
            / 65536.0
            * (
                1.0
                + float(self._dig_H6)
                / 67108864.0
                * h
                * (1.0 + float(self._dig_H3) / 67108864.0 * h)
            )
        )
        h = h * (1.0 - float(self._dig_H1) * h / 524288.0)
        return h

    def read_temperature_f(self) -> float:
        """Wrapper to get temp in F."""
        celsius = self.read_temperature()
        temp = celsius * 1.8 + 32
        return temp

    def read_pressure_inches(self) -> float:
        """Wrapper to get pressure in inches of Hg."""
        pascals = self.read_pressure()
        inches = pascals * 0.0002953
        return inches

    def read_dewpoint(self) -> float:
        """Return calculated dewpoint in C, only accurate at > 50% RH."""
        celsius = self.read_temperature()
        humidity = self.read_humidity()
        dewpoint = celsius - ((100 - humidity) / 5)
        return dewpoint

    def read_dewpoint_f(self) -> float:
        """Return calculated dewpoint in F, only accurate at > 50% RH."""
        dewpoint_c = self.read_dewpoint()
        dewpoint_f = dewpoint_c * 1.8 + 32
        return dewpoint_f

    @property
    def temperature(self) -> float:
        """Return temperature in celsius."""
        return self._temperature

    @property
    def humidity(self) -> float:
        """Return relative humidity in percentage."""
        return self._humidity

    @property
    def pressure(self) -> int:
        """Return pressure in hPa."""
        hectopascals = self._pressure
        return hectopascals

    @property
    def sample_ok(self) -> bool:
        """Returns the sensor read status."""
        return self._ok

    def update(self) -> None:
        """Read raw data and update compensated variables."""
        try:
            self._temperature = self.read_temperature()
            self._humidity = self.read_humidity()
            self._pressure = self.read_pressure()
            self._ok = True
            _LOGGER.debug(
                f'spi{self._spi_bus}.{self._spi_dev} '
                f't: {self._temperature} h: {self._humidity} p: {self._pressure}'
            )
        except BME280ReadError:
            self._ok = False
            _LOGGER.error(f'spi{self._spi_bus}.{self._spi_dev} BME280ReadError')

    def update2(self) -> None:
        """Read raw data while data don't repeat twice.
        Update compensated variables.
        """
        res_list = [[0]]
        try:
            while Counter(res_list).most_common(1)[0][1] < 2:
                temperature = self.read_temperature()
                humidity = self.read_humidity()
                pressure = self.read_pressure()
                res_list.append([temperature, humidity, pressure])
            self._temperature, self._humidity, self._pressure = Counter(
                res_list
            ).most_common(1)[0][0]
            self._ok = True
            _LOGGER.debug(f'spi{self._spi_bus}.{self._spi_dev}: {res_list}')
            _LOGGER.debug(
                f'spi{self._spi_bus}.{self._spi_dev} '
                f't: {self._temperature} h: {self._humidity} p: {self._pressure}'
            )
        except BME280ReadError:
            self._ok = False
            _LOGGER.error(f'spi{self._spi_bus}.{self._spi_dev} BME280ReadError')
