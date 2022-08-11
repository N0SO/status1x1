#!/usr/bin/env python3
from specialeventstation import specialEventStation
from time import sleep
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
			'K0E', 'N0E', 'W0E',
			'K0R', 'N0R', 'W0R',
			'K0I', 'N0I', 'W0I'	]
				
STARTDATE = 'April 3, 2022'
ENDDATE = 'April 4, 2022'
				
class moqpseReport():
    def __init__(self, calls=None, sdate=None, edate=None):
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
                            End_date=edate)})
        """    
        if calls and sdate and edate:
            self.appMain(selist, sdate, edate)
		"""
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

    se=moqpseReport(calls=SECALLS, sdate=STARTDATE, edate=ENDDATE)
    #se = moqpseReport()

    """
    for station in SECALLS:
        se.seStations[station].show_params()
    se.stations['N0H'].opcall='AB0RX'
    se.stations['W0S'].opcall='WA0JCO'
    se.stations['W0W'].opcall='AA0Z'
    """
    tsvList = se.makeTSV('SHOWME')
    tsvList = se.makeTSV('MO')
