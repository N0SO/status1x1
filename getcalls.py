#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
 
dr = webdriver.Chrome()

callspage = dr.get('http://www.1x1callsigns.org/index.php/search')
print ('callspage type: {}\n'.format(type(callspage)))
print ('callspage:\ntype: {}\ndir:\n{}\nvars:\v{}\n'.format(type(callspage), dir(callspage), vars(callspage)))
print ('callspage:\ntype: {}\ndir:\n{}\nvars:\v{}\n'.format(type(callspage), dir(callspage), vars(callspage)))

sbox=dr.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[1]/td[2]/form[1]/table[1]/tbody[1]/tr[1]/td[1]/input[1]")

# Sending input text to search field
sbox.send_keys("N0H")
     
# Pressing enter to search input text
sbox.send_keys(Keys.ENTER)
sleep(10)
tbox = dr.find_element(By.XPATH,"//td[contains(text(),'August 28, 2021')]")
#print ('tbox:\ntype: {}\ndir:\n{}\nvars:\v{}\n'.format(type(tbox), dir(tbox), vars(tbox)))
sleep(10)
