# -*- coding: utf-8 -*-
#
# reads yaml header from markdown file, translates to json for map
#

import glob
import arrow
import yaml
import re
import json
from tzwhere import tzwhere

# takes some time to initialise
tz = tzwhere.tzwhere(shapely=True, forceTZ=True)

#
# Reads yaml
#
def read_yaml(yaml_file):
    with open(yaml_file, 'r') as f:
        yml = f.read()

    return yaml.load(yml)

#
# Reads yaml from markdown file
#
def read_yaml_from_markdown(markdown_file):
    with open(markdown_file, 'r') as f:
        md = f.read()

    print("Reading {}...".format(markdown_file))

    # pyyaml doesn't like zero dates
    md = re.sub("0000-00-00 00:00:00", "", md)

    # return first yaml document
    for y in yaml.load_all(md):
        return y

#
# Parses GPS co-ordinates that were originally dumped from exif
#
def parse_exif_gps(GPSPosition, GPSAltitude):
    matches = re.match(r"(\d+). (\d+)' (\d+\.\d+)\" ([NS]), (\d+). (\d+)' (\d+\.\d+)\" ([EW])", GPSPosition)

    def dms_to_ddeg(d,m,s):
        return int(d) + int(m)/60.0 + float(s)/3600.0

    lat = dms_to_ddeg(matches.group(1),
                      matches.group(2),
                      matches.group(3))
    if lat >= 90:
        raise ValueError('latitude out of range!')
    if matches.group(4) == 'S':
        lat = -lat


    lon = dms_to_ddeg(matches.group(5),
                      matches.group(6),
                      matches.group(7))
    if lon >= 180:
        raise ValueError('longitude out of range!')
    if matches.group(8) == 'W':
        lon = -lon

    matches = re.match(r"(\d+) m Above Sea Level", GPSAltitude)
    altitude = int(matches.group(1))

    if altitude > 50e3:
        raise ValueError('altitude out of range!')

    return {
        'latitude': lat,
        'longitude': lon,
        'altitude': altitude
    }


#
# Formats datetime to human readable
#
def parse_datetime(ModifyDate, tz, location):
    if ModifyDate != None:
        arw = arrow.get(ModifyDate).replace(months=-1)

        timezone_str = tz.tzNameAt(location["latitude"],
                                   location["longitude"],
                                   forceTZ=True)

        arw = arw.to(timezone_str)

        return arw.format('D MMMM') + ' at ' + arw.format('h:mm A') + \
        ' local ' + timezone_str
    else:
        raise ValueError('Bad date')

#
# Converts image listing to json. Returns name of file written
#
def listing_to_json(flight_nr, asset_path):

    # read yaml
    try:
        filename = "img_listings/ubseds{}.markdown".format(flight_nr)
        images = read_yaml_from_markdown(filename)["images"]

        config_filename = "img_listings/ubseds{}_config.yaml".format(flight_nr)
        config = read_yaml(config_filename)
    except:
        # failed to read listing
        return None

    js_obj = []

    # takes some time to initialise
    print("Initialising timezones...")
    tz = tzwhere.tzwhere(shapely=True, forceTZ=True)

    for img in images:
        try:
            location = parse_exif_gps(img["GPSPosition"], img["GPSAltitude"])
            human_time = parse_datetime(img["ModifyDate"], tz, location)

            js_obj.append({
                'name': img['name'],
                'location': location,
                'human_time': human_time
            })
        except:
            None                # uhh just ignore bad images


    # write json
    config["json"] = asset_path + "img.json"
    json_filename = "../.." + asset_path + "img.json"

    with open(json_filename, "w") as outfile:
        json.dump(js_obj, outfile, indent=2)

    return {
        'config': config,
        'images': js_obj
    }

#
# main
#
if __name__ == "__main__":
    listing_to_json(20, '/_tools/magic-ring-binder/img_listings/')
