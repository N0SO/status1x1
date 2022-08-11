#!/usr/bin/env python3
from datetime import datetime

TIMEFMT='%B %d, %Y'

class SES():
    """
    Class sturcture to hold 1x1 Special Event Station details
    Just the data and a few simple methods to make it usefull.
    """
    def __init__(self,
                 callsign=None,
                 Start_date=None,
                 End_date=None):
        """
        Intialize the Speial Event Station data structure.
        You can pass in:
            the target 1x1 callsign (callsign='CALL')
            The event start date (Start_date='April 2, 2022')
            The event end date (End_date='April 3, 2022')
        The dates will be converted to DATETIME objects. 
        """
        self.callsign=callsign
        """
        Convert target Special Event date strings to 
        datetime objects if passed in as strings.
        """
        if isinstance(Start_date, str):
            self.tstart=datetime.strptime(Start_date, TIMEFMT)        
        else:
            self.tstart=Start_date
        if isinstance(End_date, str):
            self.tend=datetime.strptime(End_date, TIMEFMT)
        else:
            self.tend=End_date   
        
        self.opcall=None
        self.opname=None
        self.opemail=None
        self.opaddress=None
        self.opphone=None
        self.sename=None
        self.startdate=None
        self.enddate = None
        
    def get_params(self):
        """
        Return all SES parameters as a list:
            SE Callsign string
            SE Name string
            SE start date (datetime object)
            SE end date (datetime object)
            Op callsign
            Op name
            Op e-mail
            Op phone number
            Op address
            Start date for 1x1 database search
            End date for 1x1 database search    
        All parameters are strings except the dates, which are
        python DATETIME objects.
        """
        return [ self.callsign,\
                self.sename,\
                self.startdate,\
                self.enddate,\
                self.opcall,\
                self.opname,\
                self.opemail,\
                self.opphone,\
                self.opaddress,\
                self.tstart,\
                self.tend ]
                
    def get_dict(self):
        """
        Like get_params, but you get a dictionary object instead
        of a list.
        """
        return vars(self)
                
    def show_params(self):
        """
        Display the most usefull params.
        This is usefull for debugging.
        """
        fmtstg='Special Event Call: {}\n'+\
                'Special Event Name: {}\n'+\
                'Operator Call: {}\n'+\
                'Operator Name: {}\n'+\
                'Operator e-mail: {}\n'+\
                'Operator phone: {}\n'+\
                'Operator address: {}'
                
        print(fmtstg.format(  self.callsign,
                                self.sename,
                                self.opcall,
                                self.opname,
                                self.opemail,
                                self.opphone,
                                self.opaddress))
