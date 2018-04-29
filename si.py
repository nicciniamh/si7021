#!/usr/bin/python
import sys,time,si7021,json
from argparse import ArgumentParser

DEGSYM = u'\N{DEGREE SIGN}'

si = si7021.si7021()
ttype = si7021.TTYPE_DEGF
ttypes = ['c','f','b','--help']

parser = ArgumentParser()
parser.add_argument('-u', '--units', action='store', dest='units', choices=['c','f','b'], default='f',
                    help='Specify units of measure for temperature. c, f or b for both')
parser.add_argument('-p','--precise', action='store_true', default=False, dest='precise',
                    help='Use floating point precision (default is integer)')
parser.add_argument('-l','--loop', action='store_true', default=False, dest='loop',
                    help='Loop until exception')
parser.add_argument('-j','--json', action='store_true', default=False, dest='json',
                    help = 'Output in JSON format')


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
            j['humidity'] = cv(humi)
            j['temperature'] = cv(temp)
            j['units'] = ttypes[ttype].upper()
            print json.dumps(j)
        else:
            if ttype == si7021.TTYPE_BOTH:
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
    time.sleep(1)