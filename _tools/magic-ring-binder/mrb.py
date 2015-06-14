# Hello

import couchdbkit
import urllib
import wget
from datetime import datetime
import arrow
import dateutil.parser
import pyaml
import re

import distance
import countries
import receivers
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

flight_nr = input("Flight Number: ")

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
    n = input("Which payload to use? (1, 2, ...): ")
else:
    n = 1

# Use the first one
payload = payloads[n-1]
pid = payload["id"]
print "Using {}...".format(pid)
print

# =-----------------------------------------------------------------------

print "Loading view payload_telemetry/payload_time..."
print
payload_json_raw = db.view("payload_telemetry/payload_time",
                          include_docs = True,
                          startkey = [pid], endkey = [pid,[]])

# Only telemetry points above 200m are considered part of the flight
payload_json = [t for t in payload_json_raw if t['doc']['data']['altitude'] > 200]

# Extract just the data
payload_data = [t['doc']['data'] for t in payload_json]

# =-----------------------------------------------------------------------

flight_map = asset_path+"flight_map.kml"
kml.output(payload_data, "../.."+flight_map)

altitude_plot = asset_path+"altitude_plot.csv"
speed_plot = asset_path+"speed_plot.csv"

# =-----------------------------------------------------------------------

receivers = receivers.receiver_info(payload_json)
# Format to sensible string
for r in receivers:
    if 'max_distance' in r['data']:
        r['data']['max_distance'] = "{:0.1f}".format(r['data']['max_distance'])

# =-----------------------------------------------------------------------

launch_arrow = arrow.get(payload_data[0]['_parsed']['time_parsed'])
launch_date = launch_arrow.format('YYYY-MM-DD')
launch_time = launch_arrow.format('YYYY-MM-DD hh:mm:ss')

post_path = "../../_posts/{}-{}.markdown".format(launch_date, payload_name)

# =-----------------------------------------------------------------------



# =-----------------------------------------------------------------------

yaml = {
    "layout": "post",
    "title": payload_name.upper(),
    "date": launch_time,
    "categories": "hab flight",
    "flight_map": flight_map,
    "altitude_plot": altitude_plot,
    "speed_plot": speed_plot,
    "flight": {
        "total_distance": "{:0.1f}".format(distance.total(payload_data)),
        "great_circle": "{:0.1f}".format(distance.great_circle(payload_data)),
        "countries": countries.flight_countries(payload_data),
        "max_altitude": "{:0.1f}".format(distance.max_altitude(payload_data)),
        "receivers": receivers,
    },
}
yaml_str = pyaml.dumps(yaml)


# =-----------------------------------------------------------------------

try:
    # Read in the existing post as a template
    with open(post_path, 'r') as f:
        template = f.read()

    print "Reading {}...".format(post_path)

except IOError:
    # Read in a template
    with open("template.markdown", 'r') as f:
        template = f.read()

    print "Using template..."

# Substitute in the new yaml
combined = re.sub(r"---\n(.*)---\n", r"---\n{}---\n".format(yaml_str),
                  template, re.M, re.S)

# Write out to file
print "Writing {}...".format(post_path)
print
with open(post_path, 'w') as outfile:
  outfile.write(combined)
