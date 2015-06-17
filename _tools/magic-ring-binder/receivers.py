# Things about receivers

import couchdbkit

import countries
import distance

# Habitat
db = couchdbkit.Server("http://habitat.habhub.org")["habitat"]


#
# Provides a useful table of user information
#
def receiver_info(payload_json):

    receivers = {}

    # Foreach telemetry packet
    for t in payload_json:
        # For each receiver of that packet
        for callsign_thing in t['doc']['receivers']:

            callsign = str(callsign_thing)

            # Get info about this reception
            info = t['doc']['receivers'][callsign]

            if not callsign in receivers: # If it's a new one
                receivers[callsign] = {
                    'rxcount': 0,
                }

            # Listener telemetry?
            if 'latest_listener_telemetry' in info:
                ltelem = db.get(info['latest_listener_telemetry'])

                # Lookup country?
                if not 'country' in receivers[callsign]:
                    c = countries.get_country(ltelem['data'])
                    if c:
                        print "Found {} in {}".format(callsign, c['name'])
                        receivers[callsign]['country'] = c

                # Calculate great circle distance
                dist = distance.gc(ltelem['data'], t['doc']['data'])

                if not 'max_distance' in receivers[callsign]:
                    receivers[callsign]['max_distance'] = dist
                if dist > receivers[callsign]['max_distance']:
                    receivers[callsign]['max_distance'] = dist

            # Update rxcount
            receivers[callsign]['rxcount'] += 1

    rlist = []
    for callsign in receivers:
        rlist.append({
            'callsign': callsign,
            'data': receivers[callsign]
        })

    # Return sorted by rxcount
    rlist.sort(key=lambda r: -r['data']['rxcount'])

    return rlist
