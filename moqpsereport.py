#!/usr/bin/env python3
from specialeventstation import specialEventStation
from time import sleep
from htmlutils.htmldoc import *
from moqputils.configs.moqpdbconfig import YEAR
import csv
#from htmlutils import htmldoc



SECALLS = 	[	'K0S', 'N0S', 'W0S',
			'K0H', 'N0H', 'W0H',
			'K0O', 'N0O', 'W0O',
			'K0W', 'N0W', 'W0W',
			'K0M', 'N0M', 'W0M',
			'K0E', 'N0E', 'W0E',
			'K0I', 'N0I', 'W0I',
			'K0U', 'N0U', 'W0U',
			'K0R', 'N0R', 'W0R'	]
				
SHOWMELIST = [	'K0S', 'N0S', 'W0S',
		'K0H', 'N0H', 'W0H',
		'K0O', 'N0O', 'W0O',
		'K0W', 'N0W', 'W0W',
		'K0M', 'N0M', 'W0M',
		'K0E', 'N0E', 'W0E'	]
				
MOLIST =	[	'K0M', 'N0M', 'W0M',
			'K0I', 'N0I', 'W0I',
			'K0S', 'N0S', 'W0S',
			'K0S', 'N0S', 'W0S',
			'K0O', 'N0O', 'W0O',
			'K0U', 'N0U', 'W0U',
			'K0R', 'N0R', 'W0R',
			'K0I', 'N0I', 'W0I'	]
				
STARTDATE = 'April 3, 2022'
ENDDATE = 'April 4, 2022'
				
class moqpseReport():
    def __init__(self, calls=None, sdate=None, edate=None,
                       headless=True,
                       searchlimit=15):
        if calls == None:
            print('default')
            selist = SECALLS
        elif isinstance(calls, list):
            print('custom')
            selist = calls
        else:
            print('single call')
            selist = [calls]            

        self.stations = dict()
        for key in selist:
            self.stations.update({key:\
                            specialEventStation(callsign=key,
                            Start_date=sdate,
                            End_date=edate,
                            headless=headless,
                            searchlimit=searchlimit)})
        """    
        if calls and sdate and edate:
            self.appMain(selist, sdate, edate)
	"""

    """
    If the string value passed is None type, return a
    single character '-'. Added because blank callsigns
    were showing up as 'None' in html reports. 
    """
    def fix_none(self, stgval):
        if stgval == None: 
            return '-'
        else:
            return stgval

    def get_seStation(self, secall, start_d, end_d):
        self.seStations[secall] = specialEventStation(callsign=secall,
                                                   Start_date=start_d,
                                                   End_date=end_d)
                                    
    def makeTSV(self,award):
        if award.upper() == 'SHOWME':
            awlist = SHOWMELIST
            filename = 'showmestations.csv'
        else:
            awlist = MOLIST
            filename = 'mostations.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([' ','K0','N0','W0'])
            i=0
            maxl = len(awlist)
            while i<maxl:
                writer.writerow([ awlist[i][2:],
                                  self.stations[awlist[i]].opcall,
                                  self.stations[awlist[i+1]].opcall,
                                  self.stations[awlist[i+2]].opcall])
                i+=3

    def makeHTML(self):
        TABLEHEADER=[' ','K0','N0','W0']
        d = htmlDoc()
        d.openHead('{} Missouri QSO Party Special Event Stations'.format(YEAR),
			  './styles.css')
        d.closeHead()
        d.openBody()
					 
        d.add_unformated_text(\
		 """<h2 align='center'>{} Missouri QSO Party Special Event Stations</h2>""".format(YEAR))
        d.addTimeTag(prefix='Updated: ') 
		 
        d.add_unformated_text(\
		"""
		<p align="center">Thank You to our 1x1 Special Event Operators!<br>
						  You make the contest more fun for the rest of us!</p>
		""")
	
        """
        Code to get SHOWME table date goes here
        """
        showme = [TABLEHEADER]
        maxl=len(SHOWMELIST)
        i=0
        while i < maxl:
            showme.append(	[SHOWMELIST[i][2:],
                            self.fix_none(self.stations[SHOWMELIST[i]].opcall),
                            self.fix_none(self.stations[SHOWMELIST[i+1]].opcall),
                            self.fix_none(self.stations[SHOWMELIST[i+2]].opcall)] )
            i += 3
        

        d.addTable( tdata=showme, 
            header=True,
                    caption='SHOWME 1x1 Ops' )

        """
        Code to get MISSOURI table date goes here
        """
        showme = [TABLEHEADER]
        maxl=len(MOLIST)
        i=0
        while i < maxl:
            showme.append(	[MOLIST[i][2:],
                            self.fix_none(self.stations[MOLIST[i]].opcall),
                            self.fix_none(self.stations[MOLIST[i+1]].opcall),
                            self.fix_none(self.stations[MOLIST[i+2]].opcall) ])
            i += 3
        

        d.addTable( tdata=showme, 
                header=True,
                caption='MISSOURI 1x1 Ops' )
            
        d.add_unformated_text(\
        """
        <p align="center">
        As you work people in the contest with these 1x1 callsigns, the last letter
        of the 1x1 callsign may be used to spell out one letter in a phrase. The
        phrases for this year will be SHOW ME and MISSOURI. You will receive a
        handsome certificate if you complete one or both of the phrases!
        </p>
                
            <p align="center" style="font-family: Consolas, Terminal, Menlo, Arial">
        Example: n0S w0H k0O n0W k0M n0E
        </p>	  
        """)

        d.closeBody()
        d.closeDoc()

        d.showDoc()
        d.saveAndView('moqp1x1ses.html')






    def appMain(self, callList, SD, ED ):
        """
        The main method
        """
        tsvList = None
        print(callList)
        if (SD==None) or (ED==None):
            print("Start and END date parameters must be defined")
            return False
        for secall in callList:
            self.get_seStation(secall, SD, ED)
            sleep(10)
            
        with open('testdata.dat', 'w') as f:
            f.write(self.seStations)
            

            
        tsvList = self.makeTSV('SHOWME')
        return tsvList
			  
if __name__ == '__main__':

    #se=moqpseReport(calls=SECALLS, sdate=STARTDATE, edate=ENDDATE)
    se = moqpseReport()

    se.stations['K0S'].opcall=None
    se.stations['N0S'].opcall='AI6O'
    se.stations['W0S'].opcall='WA0JCO'
    se.stations['K0H'].opcall='N0ZNA'
    se.stations['N0H'].opcall='AB0RX'
    se.stations['W0H'].opcall=None
    se.stations['K0O'].opcall='N0BDS'
    se.stations['N0O'].opcall='KK0U'
    se.stations['W0O'].opcall=None
    se.stations['K0W'].opcall='K8MCN'
    se.stations['N0W'].opcall='W0PF'
    se.stations['W0W'].opcall='AA0Z'
    se.stations['K0M'].opcall='W0HBH'
    se.stations['N0M'].opcall='N0ZIB'
    se.stations['W0M'].opcall='W0MB'
    se.stations['K0E'].opcall='WB0QLU'
    se.stations['N0E'].opcall='N0NEB'
    se.stations['W0E'].opcall='WA0O'
    se.stations['K0I'].opcall='KI0I'
    se.stations['N0I'].opcall='KD0NEO'
    se.stations['W0I'].opcall='N0MII'
    se.stations['K0R'].opcall=None
    se.stations['N0R'].opcall=None
    se.stations['W0R'].opcall='W0EO'
    se.stations['K0U'].opcall='W0ECC'
    se.stations['N0U'].opcall=None
    se.stations['W0U'].opcall=None
    for station in SECALLS:
        se.stations[station].show_params()


    tsvList = se.makeTSV('SHOWME')
    tsvList = se.makeTSV('MO')
    
    htmlList = se.makeHTML()
