#!/usr/bin/env python3
"""
A collection of classes used to generate the 1x1 Special Event Station
list for the Missouri QSO Party

Update History:
* Thu Nov 17 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Inital release. Also, retirement day for me!
- Code is pretty crude, but it works.
* Sat Mar 18 2023 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - First official release
- It's been working to track the 2023 MOQP 1x1 allocations.
- Added code to support headless operation to make it
- easier  to use in automation scripts.
- Added some documentation because N0MII has expressed
- interest is looking at it.
* Sun Mar 02 2025 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.0 - Updates for 2025, fixes for Issues #5 and #6.
- The 1x1callsigns.org website has been changed - many of the form
- elemnt names, IDs and XPATHs changed, breaking this code. This was
- documented and fixed as Issue #5. There also was a problem with the
- method that simulates typing. Entering x0S, the S character was 
- dropped. So were E, U and R. This was documented and fixed as 
- Issue #7. The code was reworked to search for form and table elements
- instead of XPATH, except for some of the code that fetches operator
- details. Fields had moved, but the paths were the same.
- Also enhanced the script that runs this code. It now does a diff on
- the new data vs the old data and only uploads the new to W0MA.ORG if
- there are changes to the operator callsign(s).
- Bumping the version to 2.0.0 due to the extensive rewrites in file 
- sestationreport.py.
"""
VERSION='2.0.0'
