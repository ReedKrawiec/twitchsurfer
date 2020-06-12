from rest import TwitchClient, TwitchMetrics
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

def parse_dates(week_kde):
    WEEKDAY_DIVISIONS = [48, 96, 144, 192, 240, 288, 336]



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

def generate_streamer_schedule(streamer, twitch_client, metrics):



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

        metrics = TwitchMetrics(twitch_client)
        test = metrics.make_request("xqcow", "/recent_viewership_values")
        test = metrics.make_request("xqcow", "/stream_growth_values")
        
        test = metrics.make_request("xqcow", "/stream_history_values")
        # Start and stop times of streams
        test = metrics.make_request("xqcow", "/stream_time_values")
        print(test.json())
        generate_streamer_schedule("xQcOW", twitch_client)