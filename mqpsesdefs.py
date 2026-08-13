"""
Common definitions used for 1x1 callsign processing.

Lists of the default 1x1 special event stations for:
	SECALLS 	- Unique list of all
	SHOWMELIST 	- Calls eligible for the SHOWME award.
	MOLIST 		- Calls eligible for the MISSOURI award

Also holds:
	STARTDATE 	- Default start date used to searching 1x1callsigns.org.
	ENDDATE 	- Default end date used to searching 1x1callsigns.org.
"""

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

STARTDATE = 'April 3, 2027'
ENDDATE = 'April 4, 2027'
