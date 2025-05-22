#!/usr/bin/env python3
"""
A collection of classes and utilities used to generate the 1x1 Special 
Event Station list for the Missouri QSO Party.

Update History:
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
* Thu Nov 17 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Inital release. Also, retirement day for me!
- Code is pretty crude, but it works.
"""
VERSION='1.0.2'
