from rest import TwitchClient
from algos import plot_arr, arr_to_kde
import datetime
import pytz
import pdb
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import pickle
import sys

# the datetime library uses the local time so conversion to UTC is needed
LOCAL_TIMEZONE = "America/New_York"
naive_datetime = datetime.datetime.strptime ("2000-1-1 12:00:00", "%Y-%m-%d %H:%M:%S")

def parse_datetime(date_str):
    return pytz.UTC.localize(datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ"))

def parse_duration_delta(duration_str):
    vod_duration = None
    try:
        vod_duration = datetime.datetime.strptime(duration_str, "%Hh%Mm%Ss")
    except ValueError:
        try:
            vod_duration = datetime.datetime.strptime(duration_str, "%Mm%Ss")
        except ValueError:
            vod_duration = datetime.datetime.strptime(duration_str, "%Ss")

    vod_duration = datetime.timedelta(hours=vod_duration.hour, minutes=vod_duration.minute, seconds=vod_duration.second)
    return vod_duration

# Returns a list of vods and the pagination_cursor
# This might be really buggy. run a lot of tests
def get_vods(start_date, end_date, streamer, pagination_cursor=None):
    if start_date >= end_date:
        print("get_vods(): Start date cannot be greater than end_date")
        return

    ret_vods = []
    has_more = True

    while has_more:
        api_res = None

        # perform the request
        if pagination_cursor:
            api_res = twitch_client.make_request(("/helix/videos?user_id={}"
                                    "&first=100"
                                    "&after={}").format(streamer, pagination_cursor)).json()
        else:
            api_res = twitch_client.make_request(("/helix/videos?user_id={}"
                                    "&first=100").format(streamer)).json()

        api_data = api_res["data"]

        # Iterate through every video to see if it is within the time frame
        for vod in api_data:
            vod_duration = parse_duration_delta(vod["duration"])
            vod_end = parse_datetime(vod["created_at"]) 
            vod_start = vod_end - vod_duration

            # Write the datetime objects to the dictionary
            vod["start_time"] = vod_start
            vod["end_time"] = vod_end

            # If it is within the time frame add it to the return array
            if start_date <= vod_start <= end_date:
                ret_vods.append(vod)

            # Once the stream start times are past the timeframe break out of the pagination loop
            if vod_start < start_date:
                has_more = False

    # update the pagination cursor
    pagination_cursor = api_res["pagination"]["cursor"]

    return (ret_vods, pagination_cursor)




def generate_streamer_schedule(streamer, twitch_client):
    # Generates a weekly schedule that'll hopefully represent each streamers schedule
    # follow the 3 sd rule when detecting anomalies
    # https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
    # compute the precise time by finding the median and rounding to the nearest half-hour
    streamer_id = get_user_id(streamer)

    # NOTE: Twitch uses the UTC +0 timezone so we will too 
    local_today = datetime.datetime.now(pytz.timezone(LOCAL_TIMEZONE))
    utc_today = local_today.astimezone(pytz.utc)
    utc_week_start = utc_today - datetime.timedelta(weeks=1)

    FINAL_DATA = []

    # Begin collecting VOD data
    # How many weeks of VOD data to collect
    WEEK_DEPTH = 10
    TOTAL_VODS = 0
    for _ in range(WEEK_DEPTH):
        # TODO: support pagination
        # NOTE: This implementation WILL break without pagination support when processing vods over many weeks
        vods = get_vods(utc_week_start, utc_today, streamer_id)

        # Iterate through all of the vods within the local week and generate a schedule
        # 168 hrs in a week * 2 & sampling 30 minute intervals
        STREAM_STATUS = [0 for j in range(168 * 2)]

        for vod in vods[0]:
            status_index_start = vod['start_time'] - utc_week_start
            #status_index_end = vod['end_time'] - utc_week_start

            status_index_start = int(status_index_start.total_seconds() / 1800)
            #status_index_end = int(status_index_end.total_seconds() / 1800)
            if status_index_start >= 336:
                print("MADE A POOSIE WOOSPIE")
                pdb.set_trace()


            FINAL_DATA.append(status_index_start)
            STREAM_STATUS[status_index_start] = 1
            #for x in range(status_index_start, status_index_end):
            #    STREAM_STATUS[x] = 1


        # Keep track of the vods per week to come up with the number of clustering groups
        # TODO: probably better to use the median instead of the mean
        TOTAL_VODS += len(vods)

        # Plot the vod schedule of a streamer every week
        #plt.plot(STREAM_STATUS)
        #FINAL_DATA.append(STREAM_STATUS)

        # Update these variables per week
        utc_today = utc_week_start
        utc_week_start = utc_week_start - datetime.timedelta(weeks=1)


    
    # (SCRAPED) Begin k-means/medians
    # Kernel Density Estimation models the problem the best
    # https://scikit-learn.org/stable/modules/density.html

#   Flatten FINAL_DATA array
    #FLAT_DATA = []
    #for week in FINAL_DATA:
    #    for vod_time in range(week):
    #        FLAT_DATA.append(vod_time)

    #plot_arr(FINAL_DATA)
    # Pickle file for debugging
    pickle.dump(FINAL_DATA, open("tmp.p", "wb")) 
    # Tweak the bandwith to configure the strictness on what "counts" towards a particular streaming time
    # (remember that 1 unit = 30 minutes)
    # ie. rn, if a user streams on Monday at 11:00 and 12:00, each stream counts towards being part of the schedule
    # however, at 12:30 it does not
    arr_to_kde(FINAL_DATA, debug=True, bandwidth=2, kernel='gaussian', sample_start=0, sample_end=336, sample_num=336)
    plt.show()

def get_user_id(display_name):
    res = twitch_client.make_request("/helix/users?login=" + display_name).json()
    return res["data"][0]["id"]

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "debug":
        FINAL_DATA = pickle.load(open("tmp.p", "rb"))
        # NOTE: it might be worth looking into the kernels 'epanechnikov' and 'tophat' to provide finer details about the data 
        dbg_val = arr_to_kde(FINAL_DATA, debug=True, bandwidth=2, kernel='gaussian', sample_start=0, sample_end=336, sample_num=336)
        pdb.set_trace()
        #plt.show()
    else:
        STREAMERS = []
        # Generate a .ics file of the streamer schedules from their vods

        # Initialize the client and pass it in as an argument for the hotkey
        twitch_client = TwitchClient("gp762nuuoqcoxypju8c569th9wz7q5", "None", access_token="bgq3aphetc1h1e67jqi91jna9p1ots", refresh_token="io0mtmgwd1mb251gn96lietxx2fafqiq0hgcjlbo3thrrsva8g")
        twitch_client.login()

        generate_streamer_schedule("xQcOW", twitch_client)