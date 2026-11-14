#!/usr/bin/env python3
"""
A collection of classes and utilities used to generate the 1x1 Special 
Event Station list for the Missouri QSO Party.

Update History:
* Sat Nov 14 2026 Mike Heitmann, N0SO <n0so@arrl.net>
- V2.1.1 - Test build of version 2.1.1. Adds:
-        - Tested fix for Issue #9
-        - Tested fix for Issue #10
-        - Added code to place temorary working files to the /tmp
-          directory and remove them after the process completes.
-          The whole thing runs much faster too. This is ready to
-          merge back to the main branch.
* Fri Nov 13 2026 Mike Heitmann, N0SO <n0so@arrl.net>
- V2.1.0 - Test build of version 2.1.0. Adds:
-          Fixes for Issues 9 and 10.
-          Eliminates need for using selenium. The
-          host website added cloudflare challenges,
-          they were too hard to keep up with, but
-          interestingly, wget works! SO the code has been
-          refactored accordingly. It's not perfect, but
-          when the challenges pop up, switching to a
-          web browser overcomes it. The process is now
-          two parts:
-            1. fetching of a list of calls for each of
-               our 27 1x1 calls.
-            2. Parsing each list of calls to filter out
-               the MOQP event calls for the current year.
-         In spare time, this utility really needs a rewrite.
* Fri May 23 2025 Mike Heitmann, N0SO <n0so@arrl.net>
- V2.0.1 - Release of version 2.0.1. Adds:
-          Persistance of data in the database as table SESCALLS.
-          Reports for 1x1 station performance in csv and html.
-          Several bug fixes, including issue #8.
* Wed May 21 2025 Mike Heitmann, N0SO <n0so@arrl.net>
- V1.0.2 - Mostly working - still need HTML report format.
- V1.0.1 - Fix for Issue #8.
- Also added crude ability ro persist the 1x1 data in
- the MOQP database, generate reports from the database to
- guage 1x1 op performance. Added - new -n (--nodatabase) option
- to maintain the old, no database functionality.
- In addition to the sestationreport main, there is now a secondary
- main: mqpsestats, used to 
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
- Bumping the version to 1.0.0 due to the extensive rewrites in file 
- sestationreport.py.
* Thu Nov 17 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Inital release. Also, retirement day for me!
- Code is pretty crude, but it works.
"""
VERSION='2.1.0'
