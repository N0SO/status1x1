#!/usr/bin/env python3
from specialeventstation import specialEventStation
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
		self.seStations = dict()
		if calls == None:
			print('default')
			selist = SECALLS
		elif isinstance(calls, list):
			print('custom')
			selist = calls
		else:
			print('single call')
			selist = [calls]			

		for key in selist:
			self.seStations[key] = None
			
		if calls and sdate and edate:
			self.appMain(selist, sdate, edate)
		
	def get_seStation(self, secall, start_d, end_d):
		self.seStations[secall] = specialEventStation(callsign=secall,
                                                   Start_date=start_d,
                                                   End_date=end_d)
                                    
	def makeTSV(self,award):
		tsvList = ['K0\tN0\tW0']
		if award.upper() == 'SHOWME':
			awlist = SHOWMELIST
		else:
			awlist = MOLIST
		 
		i=3
		for call in awlist:
			if i == 3:
				i=0
				nextln = call[2] # Use char 3 as the side header
			nextln += '\t{}'.format(call)
			i += 1
			if i==3:
				tsvList.append(nextln)
		return tsvList			
	
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
			
		#tsvList = self.makeTSV('SHOWME')
		return tsvList
			  
if __name__ == '__main__':
    
	se=moqpseReport(calls=SECALLS, sdate=STARTDATE, edate=ENDDATE)
	for station in SECALLS:
		se.seStations[station].show_params()
