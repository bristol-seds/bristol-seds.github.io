# Distances and things

from geopy import distance

def gc(first, last):
    f = (first["latitude"], first["longitude"])
    l = (last["latitude"], last["longitude"])
    return distance.great_circle(f, l).kilometers


# Calculates the distance the flight traveled by summing the distance
# between telemetry points
# Flight distance in km
def total(payload_data):
    d = 0.0

    for i in range(len(payload_data)-1):
        d += gc(payload_data[i], payload_data[i+1])

    print "Total distance is {:0.1f} km ({} points)".format(d, len(payload_data))
    print
    return d

# First/last great circle
def great_circle(payload_data):
    if len(payload_data) > 0:
        d = gc(payload_data[0], payload_data[-1])
        f = (payload_data[0]["latitude"], payload_data[0]["longitude"])
        l = (payload_data[-1]["latitude"], payload_data[-1]["longitude"])

        print "Great circle distance is {:0.1f} km ({} to {})".format(d, f, l)
        print
        return d
    else:
        return 0

# Max altitude!
def max_altitude(payload_data):
    if len(payload_data) > 0:
        m = max([dp["altitude"] for dp in payload_data])/1000.0
        print "Maximum altitude is {:0.3f} km".format(m)
        print
        return m
    else:
        return 0
