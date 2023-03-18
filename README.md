# status1x1
Web Scraping Python app to collect info for this year's Missouri QSO Party 1x1 SE Stations
sestationreport --calls CALLSIGNLIST --start STARTDATE --end ENDDATE --type TYPE

##Usage:
```
Generate a report of 1x1 Special Event callsigns for the event starting on
STARTDATE and ending on ENDDATE using format TYPE. The website
http://www.1x1callsigns.org/ will be accessed to look up details for each 1x1
callsing in CALLSIGNLIST.

optional arguments:
  -h, --help            show this help message and exit
  -c CALLS, --calls CALLS
                        The list of callsigns to look up. Omit to use the
                        default SHOWME and MISSOURI lists.
  -s STARTDATE, --startdate STARTDATE
                        The starting date for the special event.
  -e ENDDATE, --enddate ENDDATE
                        The starting date for the special event.
  -t RTYPE, --rtype RTYPE
                        The report type (csv or html).
  -d, --display         Display the browser and show activity. Default is to
                        run "headless" (no display)..
  --version             Display version and exit

```

## To insall:

1. Needs the Selenium package
	- sudo pip3 install selenium  (I would check to see if there was an apt package first)

2. Needs the Crhomium Browser aChromium Driver packages
	- sudo apt-get install chromium-browser
	- sudo apt-get install chromium-chromedriver

3. Also uses modules from the moqputils collection:
 	- moqputils
 	- htmlutils
   
   
