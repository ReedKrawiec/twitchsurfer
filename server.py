# The REST API for twitchsurfer
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask import jsonify
from rest import TwitchClient, TwitchMetrics
# Generates an 'online' probability histogram at 30 minute intervals starting from Monday 
from surfer import generate_streamer_schedule
import sys

print("Setting up REST API...")
# Setup the REST API clients
twitch_client = TwitchClient("gp762nuuoqcoxypju8c569th9wz7q5", "None", access_token="bgq3aphetc1h1e67jqi91jna9p1ots", refresh_token="io0mtmgwd1mb251gn96lietxx2fafqiq0hgcjlbo3thrrsva8g")
twitch_client.login()
metrics = TwitchMetrics(twitch_client)

print("Finished REST API setup")

app = FlaskAPI(__name__)

@app.route("/get_schedule", methods=['GET'])
# TODO: implement some sort of caching system or something
def get_streamer_scheudle():
    if request.method == 'GET':
        streamer = request.args.get('streamer')
        return jsonify({
            'streamer': streamer, 
            'schedule': generate_streamer_schedule(request.args.get('streamer'), twitch_client, metrics)
            }), status.HTTP_200_OK
        #return generate_streamer_schedule(request.args.get('streamer'), twitch_client, metrics)


if __name__ == "__main__":
    app.run(debug=(len(sys.argv) == 2 and sys.argv[1] == "debug"))