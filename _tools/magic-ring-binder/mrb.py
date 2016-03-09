# Hello

import couchdbkit
import urllib
import wget
from datetime import datetime
import arrow
import dateutil.parser
import yaml
import re
import sys

import distance
import countries
import receivers
import aprs_json
import kml

import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# =---------------------------------------------------------------------

if len(sys.argv) >= 2:
    flight_nr = int(sys.argv[1])
else:
    flight_nr = input("Flight Number: ")

# =---------------------------------------------------------------------

if flight_nr == 1:
    payload_name = "buseds1"
else:
    payload_name = "ubseds{}".format(flight_nr)

asset_path = "/assets/flights/{}/".format(flight_nr)

# Make the assets directory
mkdir_p("../.."+asset_path)

# =---------------------------------------------------------------------

# Habitat
db = couchdbkit.Server("http://habitat.habhub.org")["habitat"]

# Grab the list of all payloads
payload_list = db.view("payload_configuration/name_time_created",
                       include_docs=True)

# Find the ones that match our name
payloads = [payload for payload in payload_list if (payload_name.lower()
                                                    in
                                                    payload["doc"]["name"].lower())]

# Print
print "Found {} payloads:".format(len(payloads))
for p in payloads:
    document = p["doc"]
    document["arrow"] = arrow.get(document["time_created"]).humanize()
    print "{_id}: {name} (Created {arrow})".format(**document)
    print

if len(payloads) > 1:
    if len(sys.argv) >= 3:
        n = int(sys.argv[2])
    else:
        n = input("Which payload to use? (1, 2, ...): ")
else:
    n = 1

# Use the first one
payload = payloads[n-1]
pid = payload["id"]
print "Using {}...".format(pid)
print

# =-----------------------------------------------------------------------

# Grab the list of all flights
flight_list = db.view("flight/end_start_including_payloads",
                       include_docs=False)

flights_payload_list = [f for f in flight_list if (f['key'][3] == 0)]
flights_with_pid     = [f for f in flights_payload_list if f['value'][0] == pid]

if len(flights_with_pid) < 1:
    print "Note: No flights with containing this payload found. Continuing..."
    print
else:
    print "Found {} flights:".format(len(flights_with_pid))
    for f in flights_with_pid:
        print "{id}".format(**f)
        print

# Select which flight
if len(flights_with_pid) > 1:
    if len(sys.argv) >= 4:
        n = int(sys.argv[3])
    else:
        n = input("Which flight to use? (1, 2, ...): ")
else:
    n = 1

flight = flights_with_pid[n-1]
fid = flight["id"]
print "Using {}...".format(fid)
print

# =-----------------------------------------------------------------------

print "Loading view payload_telemetry/payload_time..."
print
payload_json_raw = db.view("payload_telemetry/payload_time",
                          include_docs = True,
                          startkey = [pid], endkey = [pid,[]])

payload_json = [t for t in payload_json_raw]

# =-----------------------------------------------------------------------

aprs_rawfile = payload_name + "-rawdata.txt"

print "Loading aprs data from {}...".format(aprs_rawfile)

aprs_json = aprs_json.get_aprs_json(aprs_rawfile)

if aprs_json is None:
    print "(raw aprs data file not found)"
    print
else:
    # Add on aprs json
    payload_json.extend(aprs_json)

    print "(added {} aprs data points)".format(len(aprs_json))
    print

# =-----------------------------------------------------------------------

# Only telemetry points above 200m are considered part of the flight
payload_json = [t for t in payload_json if t['doc']['data']['altitude'] > 200]

# =-----------------------------------------------------------------------

# Sort the payload data by date
def data_timesort(datum):

    telemetry_t = arrow.get(datum['doc']['data']['time'], "HH:mm:ss")

    if 'key' in datum: # From habitat
        received_mean_t = arrow.get(datum['key'][1])

        # Correction for packets that get received the next day
        if telemetry_t.hour == 23 and received_mean_t.hour == 0:
            received_mean_t = received_mean_t.replace(hours=-1)

    else: # From some other source
        received_mean_t = arrow.get(datum['doc']['data']['date'], "YYMMDD")

    return [received_mean_t.date(), telemetry_t.timestamp]

payload_json_sorted = sorted(payload_json, key=data_timesort)

# Extract just the data
payload_data_sorted = [t['doc']['data'] for t in payload_json_sorted]

# =-----------------------------------------------------------------------

flight_map = asset_path+"flight_map.kml"
if flight_nr in [1,2,4,5]:      # Up/down
    kml.output(payload_data_sorted, "../.."+flight_map, True, "Landing")
else:                           # Float
    kml.output(payload_data_sorted, "../.."+flight_map, False, "Last Reported")

altitude_plot = asset_path+"altitude_plot.csv"
with open("../.."+altitude_plot, 'w') as outfile:
    outfile.write('time,latitude,longitude,altitude\n')
    for d in payload_data_sorted:
        if 'date' in d:
            date = d['date']
        else:
            date = "000000"

        outfile.write("{}-{},{:.6f},{:.6f},{}\n".format(
            date, d['time'], d['latitude'], d['longitude'], d['altitude']))

speed_plot = asset_path+"speed_plot.csv"

# =-----------------------------------------------------------------------

receivers = receivers.receiver_info(payload_json)
# Format to sensible string
for r in receivers:
    if 'max_distance' in r['data']:
        r['data']['max_distance'] = "{:0.1f}".format(r['data']['max_distance'])

# =-----------------------------------------------------------------------

if len(payload_data_sorted) > 0:
    launch_arrow = arrow.get(payload_data_sorted[0]['_parsed']['time_parsed'])
else:
    launch_arrow = arrow.utcnow() # Use current time for now

launch_date = launch_arrow.format('YYYY-MM-DD')
launch_time = launch_arrow.format('YYYY-MM-DD hh:mm:ss')

post_path = "../../_posts/{}-{}.markdown".format(launch_date, payload_name)

# =-----------------------------------------------------------------------

is_live = False

if len(payload_data_sorted) > 0:
    last_arrow = arrow.get(payload_data_sorted[-1]['date'])
    utc_2daysago = arrow.utcnow().replace(days=-2)

    if last_arrow < utc_2daysago: # live
        print
        print "Flight is less than 2 days old!! Setting the live flag..."
        is_live = True

# =-----------------------------------------------------------------------

post_yaml = {
    "layout": "post",
    "title": payload_name.upper(),
    "payload_title": payload_name.upper(),
    "date": launch_time,
    "categories": "hab flight",
    "flight_map": flight_map,
    "altitude_plot": altitude_plot,
    "habhub": {
        "live": "http://tracker.habhub.org/#!qm=All&q={}".format(payload["doc"]["name"]),
        "archive": "http://tracker.habhub.org/#!qm={}".format(fid)
    },
#    "speed_plot": speed_plot,
    "plots": True,
    "live": is_live,
    "flight": {
        "total_distance": "{:0.1f}".format(distance.total(payload_data_sorted)),
        "great_circle": "{:0.1f}".format(distance.great_circle(payload_data_sorted)),
        "countries": countries.flight_countries(payload_data_sorted),
        "max_altitude": "{:0.1f}".format(distance.max_altitude(payload_data_sorted)),
        "receiver_count": len(receivers),
        "receivers": receivers,
    },
}



# =-----------------------------------------------------------------------

try:
    # Read in the existing post as a template
    with open(post_path, 'r') as f:
        template = f.read()

    print "Reading {}...".format(post_path)

    # Read the yaml the already exists at the top of the file
    template_yaml_str = re.search("---\n(.*)---\n", template, re.S).group(1)
    template_yaml = yaml.load(template_yaml_str)

except IOError:
    # Read in a template
    with open("template.markdown", 'r') as f:
        template = f.read()

    print "Using template..."
    template_yaml = {}

# Combine our yaml object with the template (we take precidence)
template_yaml.update(post_yaml)

# Substitute in the new yaml
yaml_str = yaml.dump(template_yaml)
combined = re.sub(r"---\n(.*)---\n", r"---\n{}---\n".format(yaml_str),
                  template, re.M, re.S)

# Write out to file
print "Writing {}...".format(post_path)
print
with open(post_path, 'w') as outfile:
  outfile.write(combined)
