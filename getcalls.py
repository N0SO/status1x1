#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from datetime import datetime
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
        self.opphone=None
        self.sename=None
        
        #print(callsign, Start_date, End_date)
        
        if (callsign and \
            Start_date and \
            End_date):
                self.get_seCall(callsign,
                                Start_date,
                                End_date)
        
        
    def get_seCall(self, call, start_date, end_date):
        """
        Look up who holds the Special Event 1x1 callsign
        specified in call between the dates start_date and
        end_date. Populate the self.opxxxx data in the object.
        Return True if successful, or False if not found.
        """
        secall = call.upper()
        dr = webdriver.Chrome()

        dr.get('http://www.1x1callsigns.org/index.php/search')
        sleep(5)
        sbox=dr.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[1]/td[2]/form[1]/table[1]/tbody[1]/tr[1]/td[1]/input[1]")

        # Sending input text to search field
        sbox.send_keys(secall)
         
        # Pressing enter to search input text
        sbox.send_keys(Keys.ENTER)
        sleep(3)
        tbl = dr.find_element(By.XPATH,"//tbody/tr[2]/td[1]/div[1]/div[1]/table[1]").get_attribute('outerHTML')
        #print ('tbox:\ntype: {}\ndir:\n{}\nvars:\v{}\n'.format(type(tbox), dir(tbox), vars(tbox)))
        sleep(5)

        #print('tbl type is: {}'.format(type(tbl)))

        tbl_list = tbl.split('</tr>')
    
        for row in tbl_list:
            if secall in row:
                row_cells=row.split('</td>')
                i=0
                for cell in row_cells:
                    if '<td' in cell:
                        #print('CELL {}:\n{}'.format(i, cell))
                        txt=cell.split('>', 1)
                        #print ('{},  {}'.format(i, txt[1]))
                        if i==1:
                            st=datetime.strptime(txt[1],TIMEFMT)
                        elif i==2:
                            et=datetime.strptime(txt[1],TIMEFMT)
                        elif i==3:
                            sename=txt[1]
                        elif i==4:
                            morelink=txt[1]
                    i+=1
                
                #print('Starts: {} Ends: {} Event: {}\nLink: {}'\
                #            .format(st, et, sename, morelink))
                if (self.start>=st) and (self.end<=et):
                    print('Match found!')
                    break

        self.start=st
        self.end=et
        print(morelink)
        t1=morelink.split('a href="',1)
        t2=t1[1].split('">',1)
        print(t2[0])
        dr.get('http://www.1x1callsigns.org/'+t2[0])
        sleep(20)


if __name__ == '__main__':
    
    sestation = specialEventStation(callsign='N0W',
                                    Start_date='April 3, 2022',
                                    End_date='April 4, 2022')
