# Hello

import couchdbkit
import urllib
import wget
from datetime import datetime
import arrow
import json
import dateutil.parser
import yaml
import re
import sys

import datum_time
import distance
import countries
import receivers
import aprs_json
import kml
import laps
import altitude_plot
import img_listing_to_json
import image_map

import os, errno
from shutil import copyfile

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
flights_with_pid     = [f for f in flights_payload_list if pid in f['value']]

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

# Print information about the flight
flight = flights_with_pid[n-1]
fid = flight["id"]
print "Flight {} with {} payloads".format(fid, len(flight['value']))

# For each payload on the flight
for pid in flight['value']:
    payload = [p for p in payload_list if p["id"] == pid][0]
    print "{_id}: {name}".format(**payload["doc"])

print

# =-----------------------------------------------------------------------

payload_json = []

for pid in flight['value']:
    print "Loading view payload_telemetry/payload_time..."
    print
    payload_json_raw = db.view("payload_telemetry/payload_time",
                               include_docs = True,
                               startkey = [pid], endkey = [pid,[]])

    if len(payload_json_raw):
        payload_json.extend([t for t in payload_json_raw])

# =-----------------------------------------------------------------------

aprs = []

# For each payload on the flight
for pid in flight['value']:
    payload = [p for p in payload_list if p["id"] == pid][0]
    payload_name_a = payload["doc"]["name"].lower()
    aprs_rawfile = payload_name_a + "-rawdata.txt"

    print "Loading aprs data from {}...".format(aprs_rawfile)

    a_data = aprs_json.get_aprs_json(aprs_rawfile)
    if a_data:
        aprs.extend(a_data)

if len(aprs) == 0:
    print "(raw aprs data file not found)"
    print
else:
    # Add on aprs json
    payload_json.extend(aprs)

    print "(added {} aprs data points)".format(len(aprs))
    print

# Copy this aprs log to the assets directory
if os.path.exists(aprs_rawfile):
    copyfile(aprs_rawfile, "../.."+asset_path+"aprs.log")
    aprs_log = asset_path+"aprs.log"
else:
    aprs_log = False

# =-----------------------------------------------------------------------

# Only telemetry points above 200m are considered part of the flight
payload_json = [t for t in payload_json if t['doc']['data']['altitude'] > 200]

if payload_name == "ubseds14": # Filter out packet with altitude from UBSEDS14
    payload_json = [t for t in payload_json if t['doc']['data']['altitude'] != 11808]


# =-----------------------------------------------------------------------

# Sort the payload data by date
payload_json_sorted = sorted(payload_json, key=datum_time.timestamp)

# Extract just the documents
payload_docs_sorted = [t['doc'] for t in payload_json_sorted]
# Extract just the data
payload_data_sorted = [t['doc']['data'] for t in payload_json_sorted]

# =-----------------------------------------------------------------------

# Write out the flight record
with open('flight_record.json', 'w') as outfile:
    json_data = json.dumps(payload_docs_sorted, indent=4, separators=(',', ': '))
    outfile.write(json_data)

# =-----------------------------------------------------------------------

if payload_name == "ubseds14": # Filter out bad backlog altitude packets from ubseds14
    payload_data_filt = [t for t in payload_data_sorted if t['altitude'] > 10700 or t['date'] == "160307"]
elif payload_name == "ubseds15": # Filter out bad backlog packets again...
    payload_data_filt = [t for t in payload_data_sorted if t['date'] != "010102" and t['time'] != "06:24:28" and t['time'] != "12:40:56"]
elif payload_name == "ubseds18": # Filter out bad backlog packets again...
    payload_data_filt = [t for t in payload_data_sorted[1:] if t['date'] != "130907"]
elif payload_name == "ubseds20": # Filter out bad backlog packets again...
    payload_data_filt = [t for t in payload_data_sorted
                         if t['longitude'] != -19.217675 and (t['longitude'] > 8.229
                                                              or t['longitude'] < 8.228)]
elif payload_name == "ubseds23": # Filter out bad altitude...
    payload_data_filt = [t for t in payload_data_sorted if t['altitude'] < 20000]
elif payload_name == "ubseds24": # Filter out bad day
    payload_data_filt = [t for t in payload_data_sorted if t['date'] != "170407"]
elif payload_name == "ubseds25": # Filter out bad altitude point
    payload_data_filt = [t for t in payload_data_sorted if t['altitude'] != 2907]
else:
    payload_data_filt = payload_data_sorted

# =-----------------------------------------------------------------------

receivers = receivers.receiver_info(payload_json)
print
# Format to sensible string
for r in receivers:
    if 'max_distance' in r['data']:
        r['data']['max_distance'] = "{:0.1f}".format(r['data']['max_distance'])

# =-----------------------------------------------------------------------

# Start and end
if len(payload_data_sorted) > 0:
    launch_arrow = arrow.get(payload_data_filt[0]['_parsed']['time_parsed'])
    end_arrow = arrow.get(payload_data_filt[-1]['_parsed']['time_parsed'])
else:
    launch_arrow = arrow.utcnow() # Use current time for now
    end_arrow = arrow.utcnow() # Use current time for now

launch_date = launch_arrow.format('YYYY-MM-DD')
launch_time = launch_arrow.format('YYYY-MM-DD hh:mm:ss')

# Duration
da = end_arrow - launch_arrow
da_hours = da.seconds // 3600;
if da.days > 0:
    if da_hours > 0:
        duration = "{} day{}, {} hour{}".format(da.days, "s" if da.days != 1 else "", da_hours, "s" if da_hours != 1 else "")
    else:
        duration = "{} day{}".format(da.days, "s" if da.days != 1 else "")
else:
    duration = "{} hour{}".format(da_hours, "s" if da_hours != 1 else "")

print "Duration is {}".format(duration)

post_path = "../../_posts/{}-{}.markdown".format(launch_date, payload_name)

# =-----------------------------------------------------------------------

is_live = False

if len(payload_data_sorted) > 0:
    last_arrow = arrow.get(payload_data_sorted[-1]['_parsed']['time_parsed'])
    utc_2daysago = arrow.utcnow().replace(days=-2)

    if last_arrow > utc_2daysago: # live
        print "Flight is less than 2 days old!! Setting the live flag..."
        is_live = True
print

# =-----------------------------------------------------------------------

laps = laps.laps_east(payload_data_sorted)

# =-----------------------------------------------------------------------

flight_map = asset_path+"flight_map.kml"
flight_map_with_images = asset_path+"flight_map_with_images.kml"

# attempt to generate image map
image_map_link = None
images = img_listing_to_json.listing_to_json(flight_nr, asset_path)

if images:
    image_map_path = "../../_posts/{}-{}-image-map.markdown".format(
        launch_date, payload_name)

    image_map.write_image_map(flight_map, payload_name.upper(),
                              images['config'], image_map_path)

    image_map_link = "/hab/image-map/{}/{}-image-map.html".format(
        launch_arrow.format('YYYY/MM/DD'), payload_name)

# =-----------------------------------------------------------------------

# KML Map
if flight_nr in [1,2,4,5]:      # Up/down
    burst = True
    ending_name = "Landing"
else:
    burst = False
    ending_name = "Last Reported"


kml.output(payload_data_filt, "../.."+flight_map, burst, ending_name, None)

if images:
    kml.output(payload_data_filt, "../.."+flight_map_with_images, burst, ending_name, images)

# Altitude Plot
altitude_filename = asset_path+"altitude_plot.csv"
speed_filename = asset_path+"speed_plot.csv"
altitude_plot.output(altitude_filename, speed_filename, payload_data_filt)

# Speed plot (TODO)
speed_plot = asset_path+"speed_plot.csv"

# =-----------------------------------------------------------------------

post_yaml = {
    "layout": "post",
    "title": payload_name.upper(),
    "payload_title": payload_name.upper(),
    "date": launch_time,
    "categories": "hab flight",
    "flight_map": flight_map,
    "altitude_plot": altitude_filename,
    "aprs_log": aprs_log,
    "habhub": {
        "live": "http://tracker.habhub.org/#!qm=All&q={}*".format(payload_name.upper()),
        "archive": "http://tracker.habhub.org/#!qm={}".format(fid)
    },
#    "speed_plot": speed_plot,
    "plots": True,
    "live": is_live,
    "flight": {
        "total_distance": "{:0.1f}".format(distance.total(payload_data_filt)),
        "great_circle": "{:0.1f}".format(distance.great_circle(payload_data_filt)),
        "duration": duration,
        "countries": countries.flight_countries(payload_data_filt),
        "max_altitude": "{:0.1f}".format(distance.max_altitude(payload_data_filt)),
        "receiver_count": len(receivers),
        "receivers": receivers,
        "laps": laps,
    },
}

# =-----------------------------------------------------------------------

if laps > 0:
    #flight_data["laps"] = laps
    print "That's {} laps!".format(laps)
    print

if images:
    post_yaml["image_map"] = image_map_link
    post_yaml["flight_map_with_images"] = flight_map_with_images

# =-----------------------------------------------------------------------

try:
    # Read in the existing post as a template
    with open(post_path, 'r') as f:
        template = f.read()

    print "Reading {}...".format(post_path)

    # Read the yaml that already exists at the top of the file
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
