from rest import TwitchClient
import urllib.parse
import json
import sys

def read_json(file_name):
  with open(file_name) as file_point:
    result = json.load(file_point)
  return result

def write_json(file_name,data):
  with open(file_name, 'w') as file_p:
    json.dump(data, file_p)

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
  top_games_id = [x['id'] for x in get_top_games(game_limit)]
  data = []
  for game_id in top_games_id:
    query_string = query_string_builder({"game_id":game_id,"first":streamer_limit})
    url = "/helix/streams" + query_string
    result = twitch_client.make_request(url).json()['data']
    data = data + result
  return data

def record_data(user_data):
  try:
    data = read_json("data.json")
  except:
    data = {}
  #Basically ensures that the game and user entry exists
  #And increments the viewer count
  for user in user_data:
    game_id = user['game_id']
    user_name = user['user_name']
    #Game has not been recorded before
    if game_id not in data.keys():
      data[game_id] = {}
    #User has not been recorded before
    if user_name not in data[game_id].keys():
      data[game_id][user_name] = user['viewer_count']
    else:
      data[game_id][user_name] += user['viewer_count']
  write_json("data.json",data)  
  
GAME_LIMIT = 20
STREAMER_LIMIT = 10

twitch_client = TwitchClient("gp762nuuoqcoxypju8c569th9wz7q5", "None", access_token="bgq3aphetc1h1e67jqi91jna9p1ots", refresh_token="io0mtmgwd1mb251gn96lietxx2fafqiq0hgcjlbo3thrrsva8g")
twitch_client.login()

if(len(sys.argv) > 1 and sys.argv[1] == "display"):
  cache_subset = cache_data['game_ids']
  #Inverts the cache for game ids, as they were stored under "game_name:game_id"
  #Changes the format to "game_id:game_name"
  #Enables us to look up game name by id
  game_id_table = {}
  for game in cache_subset.keys():
    game_id_table[cache_subset[game]] = game
  try:
    data = read_json("data.json")
  except:
    print("Data file does not exist.")
  for game_id in data:
    print(game_id_table[game_id])
    for user in data[game_id]:
      print("\t" + user + " " + str(data[game_id][user]))
else:
  #Records the top STREAMER_LIMIT streamers for the top GAME_LIMIT games
  #Intended to be run over a long period of time, every 30 minutes or so
  record_data(game_data_collection(GAME_LIMIT,STREAMER_LIMIT))
