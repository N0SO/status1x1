#!/usr/bin/env python3
from ses import SES
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep, strftime
from datetime import datetime
import sys
"""
Time format is Month day, YEAR to match the 1x1 source web page.
April 4, 2022 for example
"""
TIMEFMT='%Y-%m-%d'
SEARCH1X1URL = 'https://www.1x1callsigns.org/1x1search.php'

class specialEventStation(SES):
    def __init__(self,
                 callsign=None,
                 Start_date=None,
                 End_date=None,
                 headless=True,
                 searchlimit=15):
        """
        Call parent class  __init__() method to initialize  structure
        """
        super().__init__(callsign, Start_date, End_date)

        if (self.callsign and \
              self.tstart and \
              self.tend):
                self.get_seCall(self.callsign,
                                self.tstart,
                                self.tend,
                                headless,
                                searchlimit)

    def get_seCall(self, call, start_date, end_date, 
                         headless = True,
                         searchlimit = 15):
        """
        Look up who holds the Special Event 1x1 callsign
        specified in call between the dates start_date and
        end_date. Populate the self.opxxxx data in the object.
        By default, it searches the first 15 records. To search more,
        add:
         searchlimit = nn (where nn is the number of records to search).
        Return True if successful, or False if not found.

        By default the code runs on a 'virtual browser', so no display
        is available (or required). This means the code may be executed
        in a terminal or script. If a display is needed for debug or
        demo, add:
         headless=False
        """
        secall = call.upper().strip()
        """
        Run headless (no display required)  unless the optional
        headless parameter is set False by the caller.
        """
        chrome_options = Options()
        if (headless):
            chrome_options.add_argument("--headless")
            # chrome_options.headless = True # also works
        
        # Set the path to the Chromedriver
        DRIVER_PATH = '/usr/bin/chromedriver'
        chrome_service = Service(DRIVER_PATH) 

        dr = webdriver.Chrome(options=chrome_options, 
                              service=chrome_service)
        
        # Navigate to the callsign search page
        try:
            print('Searching {} for {}...'.format(SEARCH1X1URL, secall))
            dr.get(SEARCH1X1URL)
            sleep(5)
        except:
            print('Exception...')
            print('Search Timeout - try again')
            exit()
 
        # Select the callsign search box
        sbox=dr.find_element(By.ID, 'callsign')
        #print(sbox)
        """
        Sending the target call to search field
        NOTE: Chromium and FireFox drivers have trouble sending some 
            characters (at least the RPI versions do). Most notably
            the 'S, E, R characters we use in our SES callsigns. 
            It would not be passed to the input box
            in the form. The work around (found on StackOverflow) was
            to call a javascript snippit to enter the text in the
            callsign search box. Use the execute_script method 
            instead of send_keys() method for the work around.
        """
        sbox.click()
        sbox.clear()
        #sbox.send_keys(secall)
        dr.execute_script("arguments[0].value = arguments[1];", sbox, secall) 
        sleep(1)
        #find and click the search button next to the callsign text box.
        search=dr.find_element(By.ID,'startd')
        search.click()
        sleep(1)

        #Find the table that contains the search results.
        #no_match = True
        #while True:
        r=0
        match = False
        try:
            table=dr.find_element(By.TAG_NAME, 'table')
            #print('raw table=\n{}'.format(table.text))
        except:
            """
            If a table is not found, this callsign is not in the
            database.  Exit
            """
            #print('table not found...')
            table = None
            
            
        if table:
            """
            Loop through the table rows searching for a date that falls
            within the limits defined by start_date and end_date.
            """
            rows=table.find_elements(By.TAG_NAME,'tr')
            #print('row count={}'.format(len(rows)))
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                #print('cell count = {}'.format(len(cells)))
                """
                If 5 or more cells:
                  cell[0] = secall
                  cell[1] = start date
                  call[2] = end date
                  call[3] = the more info (on operator) link.
                Compare these to what was passed in.
                """
                if len(cells) >= 5:
                    rcall=cells[0].text
                    st=datetime.strptime(cells[1].text, TIMEFMT)
                    et=datetime.strptime(cells[2].text, TIMEFMT)
                    sename=cells[3].text
                    morelink=cells[4]
                    #print('call: {}, start:{}, end:{}, more:{}'.format(rcall, st, et, sename, morelink.text))

                    if ((start_date>=st) and (start_date<=et)) or\
                          ((end_date>=st) and (end_date<=et)):
                        print('Match for {} found in row {}...'.format(\
                                      secall, r))
                        match = True
                        break
                r+=1
        else:
            #print('No table found...')
            pass

        if match:
            self.startdate=st
            self.enddate=et
            self.sename=sename
            morelink.click() # Move to details page using link from page
            sleep(5)
            """
            All data of interest is in column 2 (td[2]), Op name is row 6,
            op call in row 7 (tr[7]), etc.
            """
            self.opname = dr.find_element(By.XPATH, '//tbody/tr[4]/td[2]').text
            self.opcall = dr.find_element(By.XPATH, '//tbody/tr[5]/td[2]').text
            self.opaddress = dr.find_element(By.XPATH, '//tbody/tr[8]/td[2]').text
            self.opemail = dr.find_element(By.XPATH, '//tbody/tr[6]/td[2]').text
            self.opphone = dr.find_element(By.XPATH, '//tbody/tr[7]/td[2]').text
            dr.quit()
            return True
        else:
            # No match found
            print('No match found for call {}'.format(self.callsign))
            dr.quit()
            return False
            
        
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
        el=driver.find_element(By.ID, xpath)
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
