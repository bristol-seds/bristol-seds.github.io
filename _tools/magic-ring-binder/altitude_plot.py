# Output csv for an altitude plot
#

import arrow

import datum_time
import distance

#
# Output plot of all points
#
def output(altitude_filename, speed_filename, payload_data_filt):
    # Open file
    with open("../.."+altitude_filename, 'w') as outfile_altitude:
        with open("../.."+speed_filename, 'w') as outfile_speed:

            outfile_altitude.write('time,latitude,longitude,altitude\n')
            outfile_speed.write('time,ground_speed,alt_speed\n')

            if (len(payload_data_filt) < 2000):
                plot_all(payload_data_filt, outfile_altitude, outfile_speed)
            else:
                plot_one_per_hour(payload_data_filt, outfile_altitude, outfile_speed)


#
# Plots a single point
#
def plot_point(previous_d, this_d, outfile_altitude, outfile_speed):
    if 'date' in this_d:
        this_date = this_d['date']
    else:
        this_date = "000000"

    outfile_altitude.write("{}-{},{:.6f},{:.6f},{}\n".format(
        this_date, this_d['time'], this_d['latitude'], this_d['longitude'], this_d['altitude']))

    delta_t = datum_time.timestamp2(this_d) - datum_time.timestamp2(previous_d)
    if delta_t > 0:
        ground_speed = float(distance.gc(previous_d, this_d)) / delta_t
        alt_speed = float(this_d['altitude'] - previous_d['altitude']) / delta_t
    else:
        ground_speed = alt_speed = 0

    outfile_speed.write("{}-{},{},{}\n".format(
        this_date, this_d['time'], ground_speed, alt_speed))

#
# Plots all points
#
def plot_all(payload_data_filt, outfile_altitude, outfile_speed):

    previous_d = payload_data_filt[0]

    for d in payload_data_filt:
        plot_point(previous_d, d, outfile_altitude, outfile_speed)
        previous_d = d

#
# Reduces the number of points plotted to one per hour
#
def plot_one_per_hour(payload_data_filt, outfile_altitude, outfile_speed):

    old_time_str = ""
    previous_d = payload_data_filt[0]

    for d in payload_data_filt:
        if 'date' in d:
            date = d['date']
        else:
            date = "000000"

        # Time str is date + hour
        time_str = date + d['time'][:2]

        if (time_str != old_time_str):
            plot_point(previous_d, d, outfile_altitude, outfile_speed)

        old_time_str = time_str
        previous_d = d
