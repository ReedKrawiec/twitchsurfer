# The REST API for twitchsurfer
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask import jsonify
from rest import TwitchClient, TwitchMetrics
# Generates an 'online' probability histogram at 30 minute intervals starting from Monday 
from surfer import generate_streamer_schedule
from top import query_string_builder
import sys
import requests as req
import json

print("Setting up REST API...")
# Setup the REST API clients
twitch_client = TwitchClient("gp762nuuoqcoxypju8c569th9wz7q5", "None", access_token="bgq3aphetc1h1e67jqi91jna9p1ots", refresh_token="io0mtmgwd1mb251gn96lietxx2fafqiq0hgcjlbo3thrrsva8g")
twitch_client.login()
metrics = TwitchMetrics(twitch_client)

print("Finished REST API setup")

app = FlaskAPI(__name__)

def process_streamers(y):
    schedule = generate_streamer_schedule(y,twitch_client,metrics)
    is_end_time = False
    stream_times = []
    for x in range(0,336):
        if not is_end_time and schedule[x] > 0.75:
            stream_times.append(x)
            is_end_time = True
        elif is_end_time and schedule[x] < 0.75:
            stream_times.append(x)
            is_end_time = False
    return {
        "streamer":y,
        "schedule": stream_times
    }

@app.route("/get_schedule", methods=['GET'])
# TODO: implement some sort of caching system or something
def get_streamer_scheudle():
    query_string = query_string_builder({"first":20,"from_id":request.args.get("id")})
    url = "https://api.twitch.tv/helix/users/follows" + query_string
    headers = {
        "Client-ID": "sh58je5z5mtatvjc7jfc1m6bgfvt94",
        "Authorization": f"Bearer {request.args.get('access')}"
    }
    req_data = req.get(url,headers=headers).json()
    streamers_list = map(lambda y: y["to_name"],req_data["data"])
    streamers_list = list(map(process_streamers, streamers_list))
    response = jsonify(streamers_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, status.HTTP_200_OK

if __name__ == "__main__":
    app.run(debug=(len(sys.argv) == 2 and sys.argv[1] == "debug"))