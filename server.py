# The REST API for twitchsurfer
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask import jsonify
from rest import TwitchClient, TwitchMetrics
# Generates an 'online' probability histogram at 30 minute intervals starting from Monday 
from surfer import generate_streamer_schedule
from top import query_string_builder, read_json, write_json
import sys
import requests as req
import json
import datetime
import atexit
from os import path


print("Setting up REST API...")
# Setup the REST API clients
twitch_client = TwitchClient("gp762nuuoqcoxypju8c569th9wz7q5", "None", access_token="bgq3aphetc1h1e67jqi91jna9p1ots", refresh_token="io0mtmgwd1mb251gn96lietxx2fafqiq0hgcjlbo3thrrsva8g")
twitch_client.login()
metrics = TwitchMetrics(twitch_client)

print("Finished REST API setup")

app = FlaskAPI(__name__)

cache = {}
if path.exists("schedule_cache.json"):
    print("Reading cache")
    cache = read_json("schedule_cache.json")

def save_cache():
    print("Saving cache")
    write_json("schedule_cache.json",cache)
# A basic in memory cache for the schedules, saves after one call
# TODO Refresh an entry if it's too old
def get_schedule_cached(y):
    if y in cache:
        return cache[y]["schedule"]
    cache[y] = {}
    cache[y]["schedule"] = generate_streamer_schedule(y,twitch_client,metrics)
    cache[y]["date"] = datetime.datetime.now()
    return cache[y]["schedule"]

def process_streamers(y):
    print(y)
    # The percentage cutoff for when a streamer is considered live
    cutoff = 0.75
    schedule = get_schedule_cached(y)
    is_end_time = False
    stream_times = []
    # TODO Investigate this result
    # Workaround for schedule result
    if(schedule == 0.0):
        schedule = [0.0 for x in range(0,336)]
    always_live = True
    # checks if the stream never falls below the streaming threshold
    # Some streams are constantly online
    for x in range(0,336):
        if schedule[x] < cutoff:
            always_live = False;
    if always_live:
        streams_times = [0,335]
    else:
        # Creates the alternating [start_time,stop_time,start_time,stop_time]
        # formated list that represents a streamer's weekly streams
        for x in range(0,336):
            if not is_end_time and schedule[x] > cutoff:
                time = x
                if x == 0 and schedule[-1] > cutoff:
                    counter = 0
                    while schedule[counter-1] > cutoff:
                        counter -= 1
                    time = counter
                stream_times.append(time)
                is_end_time = True
            elif is_end_time and schedule[x] > cutoff and schedule[0] > cutoff and x == 335:
                counter = -1
                while schedule[counter + 1] > cutoff:
                    counter += 1
                stream_times.append(x + counter)
                is_end_time;
            elif is_end_time and schedule[x] < cutoff:
                stream_times.append(x)
                is_end_time = False

    return {                                                        
        "streamer":y,
        "schedule": stream_times
    }

# Gets all followed streams, making multiple 
# requests if one isn't sufficient
def get_followed(from_id,access_token):
    counter = 0
    total = 1
    pagination = ""
    data = []
    while counter < total:
        query_count = 100
        query_string = ""
        if pagination == "":
            query_string = query_string_builder({"first":query_count,"from_id":from_id})
        else:
            query_string = query_string_builder({"first":query_count,"from_id":from_id,"after":pagination})
        url = "https://api.twitch.tv/helix/users/follows" + query_string
        headers = {
            "Client-ID": "sh58je5z5mtatvjc7jfc1m6bgfvt94",
            "Authorization": f"Bearer {access_token}"
        }
        req_data = req.get(url,headers=headers).json()
        total = int(req_data["total"])
        counter += len(req_data["data"])
        pagination = req_data["pagination"]["cursor"]
        data.extend(req_data["data"])
    return data

def get_metadata(streamers,access):
    counter = 0
    total = len(streamers)
    data = []
    while counter < total:
        query_count = 30
        if counter + 30 > total:
            query_count = total - counter
        headers = {
            "Client-ID": "sh58je5z5mtatvjc7jfc1m6bgfvt94",
            "Authorization": f"Bearer {access}"
        }
        st = streamers[(counter):(counter + query_count)]
        query_string = query_string_builder({"login":st})
        url = "https://api.twitch.tv/helix/users" + query_string
        req_data = req.get(url,headers=headers).json()
        counter += len(req_data["data"])
        data.extend(req_data["data"])
    return data    

@app.route("/get_default",  methods=["GET"])
def get_default():
    streamers_list = ["xqcOW","trihex","MOONMOON","summit1g","shroud",
    "mang0","Tfue","Myth","TimTheTatman","DrLupo","NICKMERCS","loltyler1",
    "LIRIK","sodapoppin","Hiko","Mizkif"]
    processed_streamers = list(map(process_streamers, streamers_list))
    desc_data = get_metadata(streamers_list,"ffmpdvhstg2yex6hbkmjkraaumyake")
    for index in range(0,len(desc_data)):
        processed_streamers[index]["profile"] = desc_data[index]["profile_image_url"]
        processed_streamers[index]["description"] = desc_data[index]["description"]
    response = jsonify(processed_streamers)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, status.HTTP_200_OK

@app.route("/get_schedule", methods=['GET'])
# TODO: implement some sort of caching system or something
def get_streamer_scheudle():
    data = get_followed(request.args.get("id"),request.args.get('access'))
    # Parses the streamers list from the data glob we get
    streamers_list = list(map(lambda y: y["to_name"],data))
    # Now process the streamers to get their formatted schedules
    processed_streamers = list(map(process_streamers, streamers_list))
    processed_streamers = list(filter(lambda x: len(x["schedule"]) > 0,processed_streamers))
    streamers_to_fetch_metadata = list(map(lambda y: y["streamer"],processed_streamers))
    desc_data = get_metadata(streamers_to_fetch_metadata,"ffmpdvhstg2yex6hbkmjkraaumyake")
    for index in range(0,len(desc_data)):
        processed_streamers[index]["profile"] = desc_data[index]["profile_image_url"]
        processed_streamers[index]["description"] = desc_data[index]["description"]
    response = jsonify(processed_streamers)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, status.HTTP_200_OK

if __name__ == "__main__":
    app.run(threaded=True,debug=(len(sys.argv) == 2 and sys.argv[1] == "debug"))


atexit.register(save_cache)