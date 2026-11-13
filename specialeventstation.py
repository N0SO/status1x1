#!/usr/bin/env python3

#!/usr/bin/env python3

from ses import SES
from bs4 import BeautifulSoup
from datetime import datetime, date
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import os

TIMEFMT = '%Y-%m-%d'


class specialEventStation(SES):

    def __init__(self,
                 callsign=None,
                 Start_date=None,
                 End_date=None,
                 headless=True,
                 searchlimit=15,
                 search_dir='./callsigns',
                 details_dir='./details'):

        super().__init__(callsign, Start_date, End_date)

        self.allocations = []

        self.search_dir = Path(search_dir)
        self.details_dir = Path(details_dir)

        if self.callsign and self.tstart and self.tend:
            self.get_seCall(self.callsign,
                            self.tstart,
                            self.tend)

    def to_date(self, value):
        """Convert a string, datetime, or date to a date object."""

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        return datetime.strptime(value, TIMEFMT).date()

    def get_seCall(self, call, start_date, end_date,
                   headless=True, searchlimit=15):

        secall = call.upper().strip()

        contest_start = self.to_date(start_date)
        contest_end = self.to_date(end_date)

        # Locate the saved search-results file
        html_file = self.search_dir / f'{secall.lower()}.html'

        if not html_file.exists():
            print(f'Search file not found: {html_file}')
            return False

        print(f'Searching saved results for {secall}...')

        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        table = soup.find('table')

        if not table:
            print(f'No results table found for {secall}')
            return False

        # Examine every allocation in the search-results table
        for row in table.find_all('tr'):

            cells = row.find_all('td')

            if len(cells) < 5:
                continue

            try:
                allocation_call = cells[0].get_text(strip=True)
                allocation_start = self.to_date(
                    cells[1].get_text(strip=True))
                allocation_end = self.to_date(
                    cells[2].get_text(strip=True))
                event = cells[3].get_text(strip=True)

            except ValueError:
                continue

            link = cells[4].find('a', href=True)

            if not link:
                continue

            # Check inclusive date overlap
            if (allocation_start <= contest_end and
                    allocation_end >= contest_start):

                query = parse_qs(
                    urlparse(link['href']).query
                )

                allocation_id = query.get('byid', [None])[0]

                if not allocation_id:
                    print(f'No allocation ID for {event}')
                    continue

                detail_file = (
                    self.details_dir /
                    f'{allocation_call}_{allocation_id}.html'
                )

                print(f'Match: {allocation_call} - {event}')

                if not detail_file.exists():
                    print(f'Detail file missing: {detail_file}')
                    continue

                details = self.read_details(detail_file)

                if not details:
                    print(f'Unable to read details: {detail_file}')
                    continue

                # Combine search and detail-page information
                allocation = {
                    'call': allocation_call,
                    'start': allocation_start,
                    'end': allocation_end,
                    'event': event,
                    'id': allocation_id,
                    'detail_file': str(detail_file),
                    **details
                }

                self.allocations.append(allocation)

        if not self.allocations:
            print(f'No matching allocation found for {secall}')
            return False

        # Populate original SES attributes from first match
        first = self.allocations[0]

        self.startdate = datetime.combine(first['start'],
                                          datetime.min.time())
        self.enddate = datetime.combine(first['end'],
                                        datetime.min.time())

        self.sename = first['event']
        self.opname = first.get('opname')
        self.opcall = first.get('opcall')
        self.opaddress = first.get('opaddress')
        self.opemail = first.get('opemail')
        self.opphone = first.get('opphone')

        return True

    def read_details(self, html_file):
        """Read the two-column allocation detail table."""

        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        details = {}

        for row in soup.find_all('tr'):

            cells = row.find_all('td')

            if len(cells) < 2:
                continue

            field = cells[0].get_text(strip=True).lower()
            value = cells[1].get_text(separator=os.linesep,
                                      strip=True)

            if field == 'requestor':
                details['opname'] = value

            elif field == 'requestor call':
                details['opcall'] = value

            elif field == 'requestor addr':
                details['opaddress'] = value

            elif field == 'email':
                details['opemail'] = value

            elif field == 'phone':
                details['opphone'] = value

        return details


if __name__ == '__main__':

    import sys

    if len(sys.argv) >= 2:
        callsign = sys.argv[1].upper()
    else:
        callsign = 'K0S'

    sestation = specialEventStation(
        callsign,
        Start_date='April 03, 2027',
        End_date='April 04, 2027'
    )

    sestation.show_params()

    print('\nMatching allocations:')
    for allocation in sestation.allocations:
        print(allocation)
