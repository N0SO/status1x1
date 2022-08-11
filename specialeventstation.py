#!/usr/bin/env python3
from ses import SES
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from time import sleep, strftime
from datetime import datetime
import sys
"""
Time format is Month day, YEAR to match the 1x1 source web page.
April 4, 2022 for example
"""
TIMEFMT='%B %d, %Y'

class specialEventStation(SES):
    def __init__(self,
                 callsign=None,
                 Start_date=None,
                 End_date=None):
        """
        Call parent class  __init__() method to initialize  structure
        """
        super().__init__(callsign, Start_date, End_date)

        if (self.callsign and \
              self.tstart and \
              self.tend):
                self.get_seCall(self.callsign,
                                self.tstart,
                                self.tend)

    def get_seCall(self, call, start_date, end_date, searchlimit = 15):
        """
        Look up who holds the Special Event 1x1 callsign
        specified in call between the dates start_date and
        end_date. Populate the self.opxxxx data in the object.
        By default, it searches the first 15 records. To search more,
        add:
         searchlimit = nn (where nn is the number of records to search).
        Return True if successful, or False if not found.
        """
        secall = call.upper()
        dr = webdriver.Chrome()
        
        # Navigate to the callsign search page
        dr.get('http://www.1x1callsigns.org/index.php/search')
        sleep(5)
        
        # Select the callsign search box
        textbox_xpath = "//body[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[1]/td[2]/form[1]/table[1]/tbody[1]/tr[1]/td[1]/input[1]"
        sbox=dr.find_element(By.XPATH,textbox_xpath)

        """
        Sending the target call to search field
        NOTE: Chromium and FireFox drivers have trouble sending some 
            characters (at least the RPI versions do). Most notably
            the 'S' character. It would not be passed to the input box
            in the form. The work around (found on StackOverflow) was
            to call a javascript snippit to enter the text in the
            callsign search box. Use the method write_to_element()
            instead of send_keys() method for the work around.
        """
        #self.send_keys(sbox, secall)
        self.write_to_element(dr, textbox_xpath, secall)
        
        sleep(2)

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
                if ((start_date>=st) and (start_date<=et)) or\
                                ((end_date>=st) and (end_date<=et)):
                    print('{} Match found! {}'.format(r, secall))
                    no_match = False
                    break
                r+=1
                if r>= searchlimit:
                    break
                c=1
            c += 1
        
        if no_match:
            # No match found
            print('No match found for call {}'.format(self.callsign))
            return False
            
        self.startdate=st
        self.enddate=et
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
        
    def send_keys(self, el: WebElement, keys: str):
        """
        Send string to an element using the webdriver send_keys method.
        NOTE: This does not work for the chromium driver on an RPI.
        Use the write_to_element() method below as a work around.
        """
        for i in range(len(keys)):
            el.send_keys(keys[i])
            sleep(1)
        el.send_keys(Keys.ENTER)
        return True

    def write_to_element(self, driver, xpath, input_string): 
        """
        NOTE: Chromium and FireFox drivers have trouble sending some 
            characters (at least the RPI versions do). Most notably
            the 'S' character. It would not be passed to the input box
            in the form. The work around (found on StackOverflow) was
            to call a javascript snippit to enter the text in the
            callsign search box. Use the method write_to_element()
            instead of send_keys() method for the work around.
        """
        el=driver.find_element(By.XPATH, xpath)
        js_command = f'document.evaluate(\'{xpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = \'{input_string}\';'
        driver.execute_script(js_command)
        sleep(2)
        el.send_keys(Keys.ENTER)
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
