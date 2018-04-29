#!/usr/bin/python
import sys,time,si7021,json
from argparse import ArgumentParser

# Test Script si.py
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


DEGSYM = u'\N{DEGREE SIGN}'

si = si7021.si7021()
ttype = si7021.TTYPE_DEGF
ttypes = ['c','f','b']

parser = ArgumentParser(description='Test program for si7021 Sensor Class version %(prog)s 1.0')
parser.add_argument('-b', '--both', action='store_const', dest='units', const='b', 
                    help='Get results as both farenheit and celsius.')
parser.add_argument('-c', '--celsius', action='store_const', dest='units', const='c', 
                    help='Get results in celsius.')
parser.add_argument('-d', '--delay', action='store', dest='delay', type=float, metavar='seconds',
                    default=1.0, help='Delay in seconds and/or fraction of seconds to delay while looping.')
parser.add_argument('-f', '--farenheit', action='store_const', dest='units', const='f', 
                    help='Get results in farenheit.')
parser.add_argument('-p','--precise', action='store_true', default=False, dest='precise',
                    help='Use floating point precision (default is integer)')
parser.add_argument('-l','--loop', action='store_true', default=False, dest='loop',
                    help='Loop until exception')
parser.add_argument('-j','--json', action='store_true', default=False, dest='json',
                    help = 'Output in JSON format')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')


args = parser.parse_args()

ttype = ttypes.index(args.units)
if args.precise:
    cv = float 
else:
    cv = int

while True:
    try:
        [temp,humi] = si(ttype,args.precise)

        if args.json:
            j = {}
            if args.units == 'b':
                j['temp_c'] = cv(temp[0])
                j['temp_f'] = cv(temp[1])
            else:
                j['temp_{}'.format(ttypes[ttype].lower())] = cv(temp)
            j['humidity'] = cv(humi)
            j['units'] = ttypes[ttype].upper()
            print json.dumps(j)
        else:
            if args.units == 'b':
                print 'Both Processing'
                s = u''
                for i in range(0,2):
                    if args.precise:
                        s=s+u'{}{}{} '.format(float(temp[i]),DEGSYM,ttypes[i].upper())
                    else:
                        s=s+u'{:3d}{}{} '.format(int(temp[i]),DEGSYM,ttypes[i].upper())
            else:
                if args.precise:
                    s=u'{}{}{}'.format(float(temp),DEGSYM,ttypes[ttype].upper())
                else:
                    s=u'{:3d}{}{}'.format(int(temp),DEGSYM,ttypes[ttype].upper())
            if args.precise:
                h  = '{}%'.format(float(humi))
            else:
                h  = '{:3d}%'.format(int(humi))

            print u'Relative humidity is {}, Temperature is {}'.format(h,s)
        
    except KeyboardInterrupt as k:
        print 'Ouch {}'.format(k)
        sys.exit(0)
    except IOError as e:
        print 'Exception encountered: {}'.format(e)
    if not args.loop:
        break
    time.sleep(args.delay)
