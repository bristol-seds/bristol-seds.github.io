# Output csv for an altitude plot
#

import arrow

#
# Output plot of all points
#
def output(filename, payload_data_filt):
    # Open file
    with open("../.."+filename, 'w') as outfile:
        outfile.write('time,latitude,longitude,altitude\n')

        if (len(payload_data_filt) < 2000):
            plot_all(payload_data_filt, outfile)
        else:
            plot_one_per_hour(payload_data_filt, outfile)

#
# Plots all points
#
def plot_all(payload_data_filt, outfile):
    for d in payload_data_filt:
        if 'date' in d:
            date = d['date']
        else:
            date = "000000"

        outfile.write("{}-{},{:.6f},{:.6f},{}\n".format(
            date, d['time'], d['latitude'], d['longitude'], d['altitude']))

#
# Reduces the number of points plotted to one per hour
#
def plot_one_per_hour(payload_data_filt, outfile):

    old_time_str = ""

    for d in payload_data_filt:
        if 'date' in d:
            date = d['date']
        else:
            date = "000000"

        # Time str is date + hour
        time_str = date + d['time'][:2]

        if (time_str != old_time_str):
            outfile.write("{}-{},{:.6f},{:.6f},{}\n".format(
                date, d['time'], d['latitude'], d['longitude'], d['altitude']))

        old_time_str = time_str
