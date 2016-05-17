# Returns a list of countries the flight passed through


import json
import numpy as np
import matplotlib.path as mplPath

# Point in Polygon?
def point_in_polygon(outline, point):
    return mplPath.Path(np.array(outline)).contains_point(point)

# Checks if a point is in a country
def point_in_country(country, point):
    for outline in country['simple_outlines']:
        if point_in_polygon(outline, point):
            return True

    return False


# Load country outlines
with open('countries_world.json') as data_file:
    countries = json.load(data_file)

last_country = None
def get_country(datapoint):
    global last_country

    # Get the lon/lat point
    point = (datapoint["longitude"], datapoint["latitude"])

    # Try the last one
    if last_country:
        if point_in_country(last_country, point):
            return {"name": last_country["name"], "isocode": last_country["isocode"].lower()}

    # Search each country
    for country in countries:
        if point_in_country(country, point):
            last_country = country
            return {"name": country["name"], "isocode": country["isocode"].lower()}

    return None

def flight_countries(payload_data):

    print "Searching for countries..."
    print

    flight_countries = []
    # Foreach datapoint
    for dp in payload_data:
        # Lookup country
        c = get_country(dp)

        # If it's a country
        if c:
            # If not the last country
            if len(flight_countries) == 0 or c != flight_countries[-1:][0]:
                flight_countries.append(c)
                print "Passed through {}...".format(c["name"])

    print
    return flight_countries
