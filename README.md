# Silicon Labs si7021 Interface Class
Copyright (C) 2018 Nicole Stevens

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
    http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

This is a simple class, currently written for Python 2.7. It does basic reads of the temperature
and humidity from the si7021. This code works comfortably with Python 2 or Python 3

Requires smbus2.

 `pip install smbus2`

Module Data:
``` Python
I2C_BUS = 8             # I2C Bus Device to use. On my laptop this device is 8, see note below. 
DEVICE_ADDRESS = 0x40   # Address of the I2C device. In theory another device can be on the same bus.
TEMPERATURE = 0xE3      # Command to retrieve temperature from the device
HUMIDITY = 0xF5         # Command to retrieve the humidity from the device
# Return value format for the temperature method
TTYPE_BOTH = 2          # Return both degrees C and degrees F
TTYPE_DEGF = 1          # Return degrees F
TTYPE_DEGC = 0          # Return degrees C
```

## Usage
``` Python
import si7021
si = si7021.si7021(bus = I2C_BUS, addr = DEVICE_ADDRESS)
                Parameters:
                    bus  - i2c bus to use, default 8
                    addr - Device address to send commands to. Default 0x40

```

## Methods
### Temperature
``` Python
    temperature(rtype=TTYPE_BOTH, precise=False):
        Read temperature from device, optional parameters:
            rtype   -   TTYPE_DEGC, return in degrees C
                        TTYPE_DEGF, return in degrees F
                        TTYPE_BOTH, return list with [c,f]
            precise -   True|False, return precise or fixed number. Default false
```

###  Humidity
``` Python
    def humidity(self, precise=False):
        Read humidity from device
            precise -   True|False, return precise or fixed number. Default false
```
### Call
The call method __call__ is not called directly but as:
``` Python
    si(rtype=TTYPE_BOTH, precise=False):
            rtype   -   TTYPE_DEGC, return in degrees C
                        TTYPE_DEGF, return in degrees F
                        TTYPE_BOTH, return list with [c,f]
            precise -   True|False, return precise or fixed number. Default false
```
## Notes about the temperature and call methods:
    When TTYPE_BOTH is used as the return type, temperature is returned as a tuple containing (c,f)

## Precision
The si7021 returns temperature and humidity with high precision. The default operation of the call, temperature and humidity methods is to return a floating point number to two decimal places. By setting precise to True, the floating point number returned is as precise as the device can give. 

## Notes about my environment I use: 
My development system is a HP Laptop running Linux Mint 18.3. The I2C interface I use is a ch341a USB GPIO/I2C device. To use this device with Linux I have a kernel module by Tse Lun Bien. This, for me, creates an I2C bus number 8. I have not tested this code but it *should* work with a Raspberry PI running Raspian.

