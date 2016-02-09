# Reads aprs telem from files

import sys
import re
import aprslib

import os.path
from datetime import datetime

time_packet = re.compile(r'(.*) GMT: (.*)')

def get_aprs_json(filename):

    if not os.path.exists(filename):
        return None

    aprs_json = []
    # Foreach line
    for line in open(filename):
        if not "[Duplicate" in line: # strip duplicates

        # Extract time and packet
            match = time_packet.match(line)
            if match is not None:
                time = match.group(1)
                packet = match.group(2)

            # Process time
            dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

            # Process packet
            pkt = aprslib.parse(packet)

            # construct data
            data = {
                'date': dt.strftime("%y%m%d"),
                'time': dt.strftime("%H:%M:%S"),
                'latitude': pkt['latitude'],
                'longitude': pkt['longitude'],
                'altitude': pkt['altitude'],
            }

            # construct receivers
            receivers = {
                pkt['via']: {}
            }

            # construct doc
            doc = {
                'data': data,
                'receivers': receivers,
            }

            aprs_json.append({
                'doc': doc
            })

    return aprs_json
