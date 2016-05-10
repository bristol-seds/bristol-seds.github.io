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

                if 'latitude' in pkt and 'longitude' in pkt and 'altitude' in pkt: # valid position packet
                    # construct data
                    data = {
                        'date': dt.strftime("%y%m%d"),
                        'time': dt.strftime("%H:%M:%S"),
                        'latitude': pkt['latitude'],
                        'longitude': pkt['longitude'],
                        'altitude': pkt['altitude'],
                        '_parsed': {
                            'time_parsed': time
                        },
                    }

                    path_index = 1
                    rx_call = pkt['path'][-path_index]
                    while rx_call.startswith('T2'):
                        path_index = path_index + 1
                        rx_call = pkt['path'][-path_index]

                    # construct receivers
                    receivers = {
                        rx_call: {}
                    }

                    # construct doc
                    doc = {
                        'data': data,
                        'receivers': receivers,
                    }

                    aprs_json.append({
                        'doc': doc
                    })
                else:           # not a valid position packet. ignore for now
                    False

    return aprs_json
