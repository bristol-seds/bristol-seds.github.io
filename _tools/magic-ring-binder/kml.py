#
#
# Somewhat from habitat:
#   https://github.com/ukhas/habitat-export-payload-telemetry/blob/master/habitat_export_payload_telemetry/lists.py
#   Export Payload Telemetry
#   Adam Greig, Nov 2012
#   CouchDB List Functions
#
def output(payload_data, kml_path):

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

        launch = burst = land = name = None
        for data in payload_data:
            if not name:
                name = data['payload'] if 'payload' in data else "Unknown"
            if "latitude" in data and "longitude" in data and "altitude" in data:
                if not launch:
                    launch = burst = data
                if data["altitude"] > burst["altitude"]:
                    burst = data

                land = data
                outfile.write("{longitude},{latitude},{altitude}\r\n".format(**data))


        launch_desc = ", ".join("{0}: {1}".format(k, v) for k, v in launch.items())
        burst_desc = ", ".join("{0}: {1}".format(k, v) for k, v in burst.items())
        land_desc = ", ".join("{0}: {1}".format(k, v) for k, v in land.items())
        launch_coords = "{longitude},{latitude},{altitude}\r\n".format(**launch)
        burst_coords = "{longitude},{latitude},{altitude}\r\n".format(**burst)
        land_coords = "{longitude},{latitude},{altitude}\r\n".format(**land)

        outfile.write( """
                    </coordinates>
                </LineString>
            </Placemark>
            <name>Flight Path</name>
        </Folder>
        <name>{name} Data Export</name>
        <Folder>
            <name>Launch, Burst and Landing Points</name>
            <Placemark>
                <name>Launch</name>
                <description>{launch_desc}</description>
                <Point>
                    <extrude>0</extrude>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>{launch_coords}</coordinates>
                </Point>
            </Placemark>
            <Placemark>
                <name>Burst</name>
                <description>{burst_desc}</description>
                <Point>
                    <extrude>0</extrude>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>{burst_coords}</coordinates>
                </Point>
            </Placemark>
            <Placemark>
                <name>Landing</name>
                <description>{land_desc}</description>
                <Point>
                    <extrude>0</extrude>
                    <altitudeMode>absolute</altitudeMode>
                    <coordinates>{land_coords}</coordinates>
                </Point>
            </Placemark>
        </Folder>
    </Document>
    </kml>""".format(**locals()))
