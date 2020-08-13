from rest import TwitchClient
import urllib.parse
import json
import sys
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

print(dname)

def read_json(file_name):
  with open(file_name) as file_point:
    result = json.load(file_point)
  return result

def write_json(file_name,data):
  with open(file_name, 'w') as file_p:
    json.dump(data, file_p,default=str)

#Cache user ids and game ids to improve speed / reduce requests
try:
  cache_data = read_json("cache.json")
except:
  cache_data = {"game_ids":{},"user_ids":{}}

#Creates a query string from an object
#The argument is a dict, with keys representing the fields in the query
#Each key is a list that contains the desired inputs for that field,
#Or a single value if there is one input for that field
#{"name":["name1","name2","name3"],"number_of_results":1}
def query_string_builder(query):
  keys = query.keys()
  #Store the string as a list to make it easy to alter
  result = list()
  for key in keys:
    #Must check the type of current key
    #It can be a singular value or a list
    if type(query[key]) is list:
      #Append each value stored under that key
      for value in query[key]:
        #We have to encode spaces and special characters in the inputs
        #For example, Dota 2 must be encoded as Dota%202, encoding the space char
        value_encoded = urllib.parse.quote(str(value))
        string = "&{}={}".format(key,value_encoded)
        result = result + list(string)
    else:
      #The value is not a list, directly append it
        value_encoded = urllib.parse.quote(str(query[key]))
        string = "&{}={}".format(key,value_encoded)
        result = result + list(string)
    #Change the initial character to be a ?
    result[0] = "?"
  return "".join(result)

#Gets game ids from its name string
#Must be an exact match
#The argument is a list of game names
#Caches the game ids 
def get_game_ids(game_string_list):
  #Select the cache data we'll be checking, in this case: game_ids
  cache_subset = cache_data["game_ids"]
  #if the game's name doesn't exist as a key inside cache_subset, its id 
  #has not been cached and will have to be retrieved
  not_cached_games = [game for game in game_string_list if game not in cache_subset.keys()]
  result = {}
  #If any of the ids are not cached, preform the request
  if(len(not_cached_games) > 0):
    query_string = query_string_builder({"name":not_cached_games})
    url = "/helix/games" + query_string;
    api_res = twitch_client.make_request(url).json()['data']
    for game in api_res:
      cache_subset[game['name']] = game['id']
  for game in game_string_list:
    result[game] = cache_subset[game]
  cache_data["game_ids"] = cache_subset
  write_json("cache.json",cache_data)
  return result

def get_top_games(limit):
  #Cache the game ids as we get them, useful for later
  cache_subset = cache_data['game_ids']
  query_string = query_string_builder({"first":limit})
  url = "/helix/games/top" + query_string
  result = twitch_client.make_request(url).json()['data']
  for game in result:
    cache_subset[game['name']] = game['id']
  cache_data["game_ids"] = cache_subset
  write_json("cache.json",cache_data)
  return result


#returns the results of every query added together
def game_data_collection(game_limit,streamer_limit):
  #Gets a list of the ids of the top games, limits by game_limit
  top_games_id = [game_data['id'] for game_data in get_top_games(game_limit)]
  data = []
  for game_id in top_games_id:
    query_string = query_string_builder({"game_id":game_id,"first":streamer_limit})
    url = "/helix/streams" + query_string
    result = twitch_client.make_request(url).json()['data']
    data = data + result
  return data

def cached_game_name(game_id):
  cache_subset = cache_data['game_ids']
  #Searches the cache for a game name that corresponds
  #to the provided game_id
  for game_name in cache_subset.keys():
    stored_game_id = cache_subset[game_name]
    if stored_game_id == game_id:
      return game_name
  return -1

def parse_data(user_data):
  cache_subset = cache_data['user_ids']
  try:
    data = read_json("data.json")
  except:
    data = {}
  #Basically ensures that the game and user entry exists
  #And increments the viewer count
  for user in user_data:
    user_id = user['user_id']
    game_id = user['game_id']
    game_name = cached_game_name(game_id)
    user_name = user['user_name']
    cache_subset[user_id]= user_name
    #Game has not been recorded before
    if game_name not in data.keys():
      data[game_name] = {}
    #User has not been recorded before
    if user_name not in data[game_name].keys():
      data[game_name][user_name] = user['viewer_count']
    else:
      data[game_name][user_name] += user['viewer_count']
  cache_data['user_ids'] = cache_subset
  return data



GAME_LIMIT = 20
#Limit for now is 100 streamers
STREAMER_LIMIT = 50
#How many streamers to display in the display mode
TOP_STREAMER_CUTOFF = 10

twitch_client = TwitchClient("gp762nuuoqcoxypju8c569th9wz7q5", "None", access_token="bgq3aphetc1h1e67jqi91jna9p1ots", refresh_token="io0mtmgwd1mb251gn96lietxx2fafqiq0hgcjlbo3thrrsva8g")
twitch_client.login()

if(len(sys.argv) > 1 and sys.argv[1] == "display"):
  
  try:
    data = read_json("data.json")
  except:
    print("Data file does not exist, run the script without any arguments to collect / update viewer data.")
    exit()
  for game_name in data:
    top_streamers = []
    #Initialize a list of tuples, that will store the top streamers
    for _ in range(0,TOP_STREAMER_CUTOFF):
      top_streamers.append({"user_name":"NULL","viewer_count":-1})
    #Game data contains viewership data for each streamer
    #under a specific game id
    game_viewers_data = data[game_name]
    #Process each streamers's viewship data within the current game
    for user_name in game_viewers_data:
      viewer_count = game_viewers_data[user_name]
      for index,streamer in enumerate(top_streamers):
        saved_viewer_count = streamer["viewer_count"]
        if viewer_count > saved_viewer_count:
          #replaces 
          top_streamers = top_streamers[:index] + [{"user_name":user_name,"viewer_count":viewer_count}] + top_streamers[index:len(top_streamers)-1]
          break

    print(game_name)
    for streamer in top_streamers:
      print("\t" + streamer["user_name"] + " " + str(streamer["viewer_count"]))
else:
  #Records the top STREAMER_LIMIT streamers for the top GAME_LIMIT games
  #Intended to be run over a long period of time, every 30 minutes or so
  raw_viewers_data = game_data_collection(GAME_LIMIT,STREAMER_LIMIT)
  parsed = parse_data(raw_viewers_data)
  write_json("data.json",parsed)
