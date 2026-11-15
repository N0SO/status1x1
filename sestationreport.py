#!/usr/bin/env python3
from tempfile import TemporaryDirectory
from pathlib import  Path
import os.path, sys, subprocess
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
            "-f", "--fetch", 
            help="""Fetch the list of callsigns to look up, but
            don't process them yet. Put list of calls to fetch
            in --calls, or leave --calls empty to 
            use the default SHOWME and MISSOURI lists.""",
            action = 'store_true')

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

    parser.add_argument(\
            "-p", "--pause-before-delete", 
            help="""Pause before deleting the temporary working files
                    in /tmp/1x1-xxxxx. While it's paused you can examin
                    the working files for debugging, etc.""",
            default=False, action = 'store_true')

    parser.add_argument('-v', '--version',
                        help='Display version and exit',
                        action='version', 
                        version=f'SEStationReport: V{VERSION}')

    args = parser.parse_args()
    return args

def fetchCallList(calls, dirpath):
    """
    Fetch a list of the most recent holders of each call in the list
    'calls'. Save the list in directory ./callsigns as an html table
    """

    for call in calls:
        filename = (f'{dirpath}/{call.lower()}.html')
        url = (f'https://www.1x1callsigns.org/1x1search.php?callsign={call}')
        print(f'Fetching list for call {call}, to file {filename}...')
        try:
            subprocess.run(
                ['wget', '-q', '-O', filename, url],
                check=True
            )
        except subprocess.CalledProcessError:
            print(f'  File list fetch  failed: {url}')

if __name__ == '__main__':
    with TemporaryDirectory(prefix="1x1-") as d:
        tempdir = Path(d)
        #tempdir = Path('/tmp/dbtemp')
        # Create working folders in the new temp directory
        if tempdir:
            dirpath = Path(f'{tempdir}/callsigns')
            detailpath = Path(f'{tempdir}/details')
        else:
            dirpath = Path('./callsigns')
            detailpath  = Path('./details')

        Path(dirpath).mkdir(parents=True, exist_ok=True)
        Path(detailpath).mkdir(parents=True, exist_ok=True)

        print (f'Temp files  path is {tempdir}')

        args = parseMyArgs()

        fetchCallList(args.calls, dirpath)
        if args.fetch:
            exit()

        if args.nodatabase:
            from moqpsereport import moqpseReport
            se=moqpseReport(args.calls,
                        args.startdate,
                        args.enddate,
                        args.display,
                        tempdir=tempdir)
        else:
            from moqpsereport import moqpDBseReport
            se=moqpDBseReport(args.calls,
                              args.startdate,
                              args.enddate,
                              args.display,
                              tempdir=tempdir)

        oplist = se.makeOplist(args.calls)
        tsvList = se.makeTSV('SHOWME')
        tsvList = se.makeTSV('MO')
        htmlList = se.makeHTML()

        # Use the -p or --pause-before-delete option to pause
        # before the temporary files used in processing are
        # deleted. Usefull for debugging!
        if args.pause_before_delete:
            breakpoint()

