#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from datetime import datetime
import sys
"""
Time format is Month day, YEAR to match the 1x1 source web page.
April 4, 2022 for example
"""
TIMEFMT='%B %d, %Y'

class specialEventStation():
    
    def __init__(self,
                 callsign=None,
                 Start_date=None,
                 End_date=None):
        """
        Intialize the data structure and look up
        the SE call if initialization data provided.
        """
        
        self.callsign=callsign
        self.start=datetime.strptime(Start_date, TIMEFMT)
        self.end=datetime.strptime(End_date, TIMEFMT)
        
        self.opcall=None,
        self.opname=None,
        self.opemail=None,
        self.opaddress=None
        self.opphone=None
        self.sename=None
        
        #print(callsign, Start_date, End_date)
        
        if (callsign and \
            Start_date and \
            End_date):
                self.get_seCall(callsign,
                                Start_date,
                                End_date)
        
    def get_params(self):
        return  self.callsign,\
                self.sename,\
                self.opcall,\
                self.opname,\
                self.opemail,\
                self.opphone,\
                self.opaddress
                
    def show_params(self):
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
                
        
    def get_seCall(self, call, start_date, end_date):
        """
        Look up who holds the Special Event 1x1 callsign
        specified in call between the dates start_date and
        end_date. Populate the self.opxxxx data in the object.
        Return True if successful, or False if not found.
        """
        secall = call.upper()
        dr = webdriver.Chrome()
        
        # Navigate to the callsign search page
        dr.get('http://www.1x1callsigns.org/index.php/search')
        sleep(3)
        
        # Select the callsign search box
        sbox=dr.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[1]/td[2]/form[1]/table[1]/tbody[1]/tr[1]/td[1]/input[1]")

        # Sending the target call to search field
        sbox.send_keys(secall)
        sleep(3) 
        
        # Pressing enter to search input text
        sbox.send_keys(Keys.ENTER)
        sleep(10)

        # Iterate thru table elements until a date match is found.
        r=c=1
        fmtstg = "//body[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/div[1]/table[1]/tbody[1]/tr[{}]/td[{}]"

        no_match = True
        while True:
            pathstg = fmtstg.format(r, c)
            try:
                tbox = dr.find_element(By.XPATH, pathstg)
            except:
                #Element not found or does not exist
                break
            if c==1:
                rcall=tbox.text
            elif c==2:
                st=datetime.strptime(tbox.text, TIMEFMT)
            elif c==3:
                et=datetime.strptime(tbox.text, TIMEFMT)
            elif c==4:
                sename=tbox.text
            elif c==5:
                morelink=tbox.text
                if (self.start>=st) and (self.end<=et):
                    print('{} Match found! {}'.format(secall,
                                                        self.callsign))
                    no_match = False
                    break
                r+=1
                c=1
            c += 1
        
        if no_match:
            # No match found
            print('No match found for call {}'.format(self.callsign))
            return False
            
        self.start=st
        self.end=et
        self.sename=sename
        tbox.click() # Move to details page using link from page
        sleep(5)
        """
        All data of interest is in column 2 (td[2]), Op name is row 6,
        op call in row 7 (tr[7]), etc.
        """
        self.opname = dr.find_element(By.XPATH, '//tbody/tr[6]/td[2]').text
        self.opcall = dr.find_element(By.XPATH, '//tbody/tr[7]/td[2]').text
        self.opaddress = dr.find_element(By.XPATH, '//tbody/tr[8]/td[2]').text
        self.opemail = dr.find_element(By.XPATH, '//tbody/tr[9]/td[2]').text
        self.opphone = dr.find_element(By.XPATH, '//tbody/tr[10]/td[2]').text
        return True
        
if __name__ == '__main__':
    
    if len(sys.argv) >=2:
        callsign = sys.argv[1].upper()
    else:
        callsign = 'N0H'
    
    sestation = specialEventStation(callsign,
                                    Start_date='April 3, 2022',
                                    End_date='April 4, 2022')
                                    
    sestation.show_params()
    print(vars(sestation))
