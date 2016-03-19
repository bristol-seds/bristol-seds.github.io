# Counts the number of times it laps the world in an eastwards direction
#
# Actually defines a lap as getting to the -180 to -90 quadrant, then the launch longitude

# Returns the number of laps the payload goes through
# Oh so lazy
def laps_east(payload_data):

    laps_east = 0

    if len(payload_data) > 0:
        launch_lon = payload_data[0]['longitude']
        i = 0

        while 1:
            for j in range(4):
                # Get to the back quadrant
                while payload_data[i]["longitude"] > -90:
                    i = i + 1
                    if i >= len(payload_data):
                        return laps_east # breakout

                # Then the launch longitude
                while payload_data[i]["longitude"] < launch_lon:
                    i = i + 1
                    if i >= len(payload_data):
                        return laps_east # breakout

            # that's a lap
            laps_east = laps_east + 1
    else:
        return 0
