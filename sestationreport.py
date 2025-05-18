#!/usr/bin/env python3
import os.path, sys
from devmodpath.devmodpath import devModPath

"""
 Add necessary dependent module paths. This can also be a file
 path to a text file containing a list of modules. Note that this
 should be removed if we ever setup an installer and put the dependant
 modules in the appropriate location.

p = devModPath(pypath = ['/home/pi/Projects/moqputils',
                         '/home/pi/Projects/cabrillolog'],
               sharepath = '/home/pi/Projects/moqputils/share')
""" 
MODPATH = devModPath(\
                pypath = '/home/pi/Projects/status1x1/pathlist.txt')

import argparse
from __init__ import VERSION
from moqpsereport import moqpseReport

USAGE = \
"""
sestationreport --calls CALLSIGNLIST --start STARTDATE --end ENDDATE --type TYPE
"""

DESCRIPTION = \
"""
Generate a report of 1x1 Special Event callsigns for the event
starting on STARTDATE and ending on ENDDATE using format TYPE.

The website http://www.1x1callsigns.org/ will be accessed to 
look up details for each 1x1 callsing in CALLSIGNLIST.
"""

def parseMyArgs():
    parser = argparse.ArgumentParser(\
                    description = DESCRIPTION, usage = USAGE)
    parser.add_argument(\
            "-c", "--calls", 
            help="""The list of callsigns to look up. Omit to 
            use the default SHOWME and MISSOURI lists.""",
            default= None)

    parser.add_argument(\
            "-s", "--startdate", 
            help="""The starting date for the special event.""",
            default=None)

    parser.add_argument(\
            "-e", "--enddate", 
            help="""The starting date for the special event.""",
            default=None)

    parser.add_argument(\
            "-t", "--rtype", 
            choices = ['csv','html'],
            default = 'csv',
            help="""The report type (csv or html).""")

    parser.add_argument(\
            "-d", "--display", 
            help="""Display the browser and show activity.
                    Default is to run "headless" (no display)..""",
            default=True, action = 'store_false')

    parser.add_argument('--version',
                        help='Display version and exit',
                        action='version', 
                        version=f'SEStationReport: V{VERSION}')

    args = parser.parse_args()
    return args
    
    
if __name__ == '__main__':
    args = parseMyArgs()

    se=moqpseReport(args.calls, 
                    args.startdate, 
                    args.enddate,
                    args.display)
    tsvList = se.makeTSV('SHOWME')
    tsvList = se.makeTSV('MO')
    htmlList = se.makeHTML()
    oplist = se.makeOplist()
