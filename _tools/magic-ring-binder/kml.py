# Outputs KMLs for map display
#

import arrow

#
# Description that appears in placemark bubble
#
def description_text(datapoint):
    if datapoint:
        time_arrow = arrow.get(datapoint['_parsed']['time_parsed'])
        time_str = time_arrow.format('DD MMMM YYYY HH:mm:ss')

        return "{}: ({latitude:.4f}, {longitude:.4f}) @ {altitude:.0f} m".format(time_str, **datapoint)
    else:
        return ""

#
# Outputs image placemark
#
def image_placemark(outfile, img, config):

    img.update(config)
    img.update(img["location"])

    outfile.write("""
            <Placemark>
                <name>{name}</name>
                <description>
                    <p>Taken {human_time}</p>
                    <p>{altitude}m altitude.
                        <a href="{page}#{name}">
                            View Full Size
                        </a>
                    </p>
                    <a href="{page}#{name}">
                        <img src="{root}/png_thumb/{name}.png"/>
                    </a>
                </description>
                <Point>
                    <extrude>0</extrude>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>{longitude},{latitude},{altitude}</coordinates>
                </Point>
            </Placemark>""".format(**img))

# <Placemark>
#     <name>Eiffel Tower</name>
#     <description>
#         Located in Paris, France.

#         This description balloon opens
#         when the Placemark is loaded.
#     </description>
#     <gx:balloonVisibility>1</gx:balloonVisibility>
#     <Point>
#       <coordinates>2.294785,48.858093,0</coordinates>
#     </Point>
#   </Placemark>

#
# Somewhat from habitat:
#   https://github.com/ukhas/habitat-export-payload-telemetry/blob/master/habitat_export_payload_telemetry/lists.py
#   Export Payload Telemetry
#   Adam Greig, Nov 2012
#   CouchDB List Functions
#
def output(payload_data, kml_path, does_burst, ending_name, images):

    new_linestring = """
                    </coordinates>
                </LineString>
            </Placemark>
            <Placemark>
                <name>Track Segment</name>
                <styleUrl>#ept</styleUrl>
                <LineString>
                    <extrude>1</extrude>
                    <tessellate>1</tessellate>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>
    """

    print "Writing {}...".format(kml_path)
    print
    with open(kml_path, 'w') as outfile:

        outfile.write("""<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://earth.google.com/kml/2.0">
    <Document>
        <Style id="ept">
            <PolyStyle>
                <color>33ffffff</color>
            </PolyStyle>
        </Style>
        <Folder>
            <Placemark>
                <name>Track Segment</name>
                <styleUrl>#ept</styleUrl>
                <LineString>
                    <extrude>1</extrude>
                    <tessellate>1</tessellate>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>
    """)

        launch = burst = ending = name = None
        last_longitude = None
        for data in payload_data:
            if not name:
                name = data['payload'] if 'payload' in data else "Unknown"
            if "latitude" in data and "longitude" in data and "altitude" in data:
                if not launch:
                    launch = burst = data
                if data["altitude"] > burst["altitude"]:
                    burst = data

                ending = data

                if last_longitude:
                    if last_longitude > 90 and data["longitude"] < -90: # Cross the antiprime meridian
                        # Write final point of linestring
                        data["longitude"] += 360
                        outfile.write("{longitude},{latitude},{altitude}\r\n".format(**data))
                        data["longitude"] -= 360

                        # Start a new one
                        outfile.write(new_linestring)

                last_longitude = data["longitude"] # Save last longitude
                outfile.write("{longitude},{latitude},{altitude}\r\n".format(**data))


        launch_desc = description_text(launch)
        burst_desc = description_text(burst)
        ending_desc = description_text(ending)

        # Launch location
        if launch:
            launch_coords = "{longitude},{latitude},{altitude}\r\n".format(**launch)
        else:
            launch_coords = ""
        # Burst location
        if burst:
            burst_coords = "{longitude},{latitude},{altitude}\r\n".format(**burst)
        else:
            burst_coords = ""
        # Ending location
        if ending:
            ending_coords = "{longitude},{latitude},{altitude}\r\n".format(**ending)
        else:
            ending_coords = ""

        if does_burst:
            points_title = "Launch, Burst and {} Points".format(ending_name)
        else:
            points_title = "Launch and {} Points".format(ending_name)

        outfile.write("""
                    </coordinates>
                </LineString>
            </Placemark>
            <name>Flight Path</name>
        </Folder>
        <name>{name} Data Export</name>
        <Folder>
            <name>{points_title}</name>
            <Placemark>
                <name>Launch</name>
                <description>{launch_desc}</description>
                <Point>
                    <extrude>0</extrude>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>{launch_coords}</coordinates>
                </Point>
            </Placemark>""".format(**locals()))

        if does_burst:
            outfile.write("""
            <Placemark>
                <name>Burst</name>
                <description>{burst_desc}</description>
                <Point>
                    <extrude>0</extrude>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>{burst_coords}</coordinates>
                </Point>
            </Placemark>""".format(**locals()))

        outfile.write("""
            <Placemark>
                <name>{ending_name}</name>
                <description>{ending_desc}</description>
                <Point>
                    <extrude>0</extrude>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>{ending_coords}</coordinates>
                </Point>
            </Placemark>""".format(**locals()))

        # images
        if images:
            for img in images['images']:
                image_placemark(outfile, img, images['config'])

        # end
        outfile.write("""
        </Folder>
    </Document>
    </kml>""")
