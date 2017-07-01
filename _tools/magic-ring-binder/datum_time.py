# Find the timestamp of a given datum
#

import arrow

def timestamp(datum):

    try:
        telemetry_t = arrow.get(datum['doc']['data']['time'], "HH:mm:ss")
    except:
        telemetry_t = arrow.get(datum['doc']['data']['time'], "HH:mm").replace(minutes=+1)
        datum['doc']['data']['time'] = telemetry_t.format("HH:mm:ss")

    if 'key' in datum: # From habitat
        received_mean_t = arrow.get(datum['key'][1])

        if str(received_mean_t) == '2017-02-19T17:54:31+00:00':
            # messed up at this time for UBSEDS21, need to extract from telem
            ts = datum['doc']['data']['_sentence']
            telemetry_t = arrow.get(ts[11:19], "HH:mm:ss")
            received_mean_t = arrow.get(ts[20:26], "YYMMDD")

        # Correction for packets that get received the next day
        if telemetry_t.hour == 23 and received_mean_t.hour == 0:
            received_mean_t = received_mean_t.replace(hours=-1)

    else: # From some other source
        received_mean_t = arrow.get(datum['doc']['data']['date'], "YYMMDD")

    # Combine date and time timestamps
    return [received_mean_t.date(), telemetry_t.timestamp]

#
#
#
def timestamp2(datum):

    try:
        telemetry_t = arrow.get(datum['time'], "HH:mm:ss")
    except:
        telemetry_t = arrow.get(datum['time'], "HH:mm").replace(minutes=+1)
        datum['time'] = telemetry_t.format("HH:mm:ss")

    if 'key' in datum: # From habitat
        received_mean_t = arrow.get(datum['key'][1])

        if str(received_mean_t) == '2017-02-19T17:54:31+00:00':
            # messed up at this time for UBSEDS21, need to extract from telem
            ts = datum['_sentence']
            telemetry_t = arrow.get(ts[11:19], "HH:mm:ss")
            received_mean_t = arrow.get(ts[20:26], "YYMMDD")

        # Correction for packets that get received the next day
        if telemetry_t.hour == 23 and received_mean_t.hour == 0:
            received_mean_t = received_mean_t.replace(hours=-1)

    else: # From some other source
        received_mean_t = arrow.get(datum['date'], "YYMMDD")

    # Combine date and time timestamps
    timestamp = received_mean_t.timestamp + telemetry_t.timestamp

    print(timestamp)

    return timestamp
