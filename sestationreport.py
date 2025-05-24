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
from mqpsesdefs import *

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
            default= SECALLS)

    parser.add_argument(\
            "-s", "--startdate", 
            help="""The starting date for the special event. Omit this
                    to use the default dates in mqpsesdefs.py""",
            default=STARTDATE)

    parser.add_argument(\
            "-e", "--enddate", 
            help="""The ending date for the special event. Omit this
                    to use the default dates in mqpsesdefs.py""",
            default=ENDDATE)

    parser.add_argument(\
            "-t", "--rtype", 
            choices = ['csv','html'],
            default = 'csv',
            help="""The report type (csv or html).""")

    parser.add_argument(\
            "-d", "--display", 
            help="""Display the browser and show activity.
                    Default is to run "headless" (no display).""",
            default=True, action = 'store_false')

    parser.add_argument(\
            "-n", "--nodatabase", 
            help="""Lookup the list of callsigns, but skip writing or
                    persisting the results in the MOQP database.""",
            default=False, action = 'store_true')


    parser.add_argument('-v', '--version',
                        help='Display version and exit',
                        action='version', 
                        version=f'SEStationReport: V{VERSION}')

    args = parser.parse_args()
    return args
    
    
if __name__ == '__main__':
    args = parseMyArgs()

    if args.nodatabase:
        from moqpsereport import moqpseReport
        se=moqpseReport(args.calls, 
                        args.startdate, 
                        args.enddate,
                        args.display)
    else:
        from moqpsereport import moqpDBseReport
        se=moqpDBseReport(args.calls, 
                        args.startdate, 
                        args.enddate,
                        args.display)
                        
    oplist = se.makeOplist(args.calls)
    tsvList = se.makeTSV('SHOWME')
    tsvList = se.makeTSV('MO')
    htmlList = se.makeHTML()
