#!/usr/bin/env python2.7

#
# Silicon Labs si7021 Interface Class
# Copyright (C) 2018 Nicole Stevens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import smbus,time
DEVICE_ADDRESS = 0x40
TEMPERATURE = 0xE3
HUMIDITY = 0xF5
I2C_BUS = 8
TTYPE_BOTH = 2
TTYPE_DEGF = 1
TTYPE_DEGC = 0


class si7021:
    """ Silicon Labs si7021 Interface Class
        Copyright (C) 2018 Nicole Stevens

        Simple class to read from the si7021 high 
        precision temperature and humidity I2C sensor.
    """
    def __init__(self,bus = I2C_BUS, addr = DEVICE_ADDRESS):
        """ Constructor: 
                Parameters:
                    bus  - i2c bus to use, default 8
                    addr - Device address to send commands to. Default 0x40

            If the device does not exist on addr IOError gets thrown by the smbus library.
        """
        self.bus = smbus.SMBus(bus)
        self.addr = addr

    def _fix_precision(self, num):
        """ Fix Precision of float to 2 decimal places """
        num = int(num*100)
        return float(num)/100.0

    def temperature(self,rtype=TTYPE_BOTH, precise=False):
        """ Read temperature from device, optional parameters:
            rtype   -   TTYPE_DEGC, return in degrees C
                        TTYPE_DEGF, return in degrees F
                        TTYPE_BOTH, return list with [c,f]
            precise -   True|False, return precise or fixed number. Default false
        """
        if rtype < 0 or rtype > 3:
            raise ValueError('Rtype must be between 0 and 2')

        [msb,lsb] = [0,0]
        while msb == 0:
            [msb,lsb] = self.bus.read_i2c_block_data(DEVICE_ADDRESS,TEMPERATURE,2)
            if msb == 0 or msb == 0xff:
                msb = 0
                time.sleep(.3)
        tempc = ((msb * 256 + lsb) * 175.72 / 65536.0) - 46.85
        tempf = (tempc * 1.8 + 32.0)
        if not precise:
            tempc = self._fix_precision(tempc)
            tempf = self._fix_precision(tempf)
        rvals = [tempc, tempf,(tempc, tempf)]
        return rvals[rtype]

    def humidity(self, precise=False):
        """ Read humidity from device
            precise -   True|False, return precise or fixed number. Default false
        """
        [msb,lsb] = [0,0]
        while msb == 0:
            self.bus.write_byte(DEVICE_ADDRESS,HUMIDITY)
            time.sleep(.3)
            [msb,lsb] = self.bus.read_byte(DEVICE_ADDRESS), self.bus.read_byte(DEVICE_ADDRESS)

        humidity = (((msb * 256 + lsb) * 125.0) / 65536.0) - 6
        if not precise:
            humidity = self._fix_precision(humidity)
        return humidity

    def __call__(self,rtype=TTYPE_BOTH, precise=False):
        t = self.temperature(rtype,precise)
        h = self.humidity(precise)
        return (t,h)
