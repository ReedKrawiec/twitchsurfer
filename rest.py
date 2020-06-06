import webbrowser
import http
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
import pdb
import threading
import urllib.parse as urlparse
from urllib.parse import parse_qs
import requests

class RESTClient(object):
    ENDPOINT = None

    def __init__(self, endpoint):
        self.ENDPOINT = endpoint

    def make_request(self, path, type="get", **headers):
        if type.lower() == "get":
            return requests.get(self.ENDPOINT + path, headers=headers)
        elif type.lower() == "post":
            return requests.post(self.ENDPOINT + path, headers=headers)


class TwitchClient(RESTClient):
    client_id = None
    oauth_code = None
    access_token = None
    client_secret = None
    refresh_token = None

    def make_request(self, path, type="get", **headers):
        if self.access_token == None:
            print("ERROR: access token not set. don't forget to run init()")

        # Setup authentication headers
        headers['Client-ID'] = self.client_id
        headers['Authorization'] = "Bearer " + self.access_token 
        response = super().make_request(path, type=type, **headers)


        #https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        # Case that the authorization token has expired
        # 401 - Unauthorized errors
        if response.status_code == 401:
            print("A token refresh is needed")
            self.refresh_oauth_access_token()
            # Make the request again after updating the access token
            headers['Authorization'] = "Bearer " + self.access_token 
            response = super().make_request(path, type=type, **headers)
        elif int(((response.status_code / 100) % 10)) != 2:
            print(response.json())

        return response


    # Simple GET request handler that parses query strings for the oauth_code
    class TokenRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                # TODO: this seems chunky
                parsed = urlparse.urlparse(self.path)
                code = parse_qs(parsed.query)['code'][0]
                self.server.callback(code)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("DonBot is now logged in. You can close this browser window now".encode())
                self.server.shutdown()
            def log_message(self, format, *args):
                print("Access token recieved!")
                return

    # Extension of ThreadingHTTPServer that has support for a callback function
    class OAuthServer(ThreadingHTTPServer):
        callback = None
        def __init__(self, address, callback, handler_class=None):
            super().__init__(address, handler_class)
            self.callback = callback

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        super().__init__("https://api.twitch.tv") 
        self.client_secret = client_secret    
        self.client_id = client_id
        self.access_token = access_token
        self.refresh_token = refresh_token

    def set_access_token(self, token):
        self.access_token = token

    # Callback function for the OAuthServer
    def set_oauth_code(self, code):
        self.oauth_code = code

    # Runs the OAuth authoriation code flow
    # Returns the auth_token to be saved
    def login(self):
        if self.access_token != None and self.refresh_token != None:
            return (self.access_token, self.refresh_token)

        self.request_oauth_code()
        return self.request_oauth_access_token()

    # sets access_token of self
    def request_oauth_code(self):
        if self.oauth_code:
            return

        # Startup a simple http server to catch the oauth request and pass it to a back to the TwitchClient through a callback
        oauth_server = TwitchClient.OAuthServer(('', 80), self.set_oauth_code ,handler_class=TwitchClient.TokenRequestHandler)
        server_thread = threading.Thread(target=oauth_server.serve_forever, args=())
        server_thread.start()

        print("You will now be asked to login to your Twitch account. Permission to edit clips is needed to create clips")
        login_url = ("https://id.twitch.tv/oauth2/authorize?client_id={}"
                            "&redirect_uri={}"
                            "&response_type={}"
                            "&scope={}").format(self.client_id, "http://localhost", "code", "clips:edit")
        print("Redirecting your browser to: " + login_url)
        webbrowser.open(login_url)

        # Wait for the server thread to shutdown and then continue. Before the shutdown self.oauth_code is set
        server_thread.join()

    # Sets the twitch client tokens and returns them as a tuple
    def refresh_oauth_access_token(self):
        oauth_client = RESTClient("https://id.twitch.tv")
        token_url = ("/oauth2/token?client_id={}"
                                   "&client_secret={}"
                                   "&refresh_token={}"
                                   "&grant_type=refresh_token"
                                   "&redirect_uri={}").format(self.client_id, self.client_secret, self.refresh_token, "http://localhost")
        token_response = oauth_client.make_request(token_url, type="post")
        if token_response.status_code != 200:
            print("The refresh token may have expired. A re-login is required")
            self.login()

        token_response = token_response.json()
        self.access_token = token_response['access_token']
        self.refresh_token = token_response['refresh_token']

        return (self.access_token, self.refresh_token)


    # Once the oauth_code is retrieved get the access_token and refresh token
    def request_oauth_access_token(self):
        if self.oauth_code == None:
            print("Cannot request OAuth token without a code")
            return

        oauth_client = RESTClient("https://id.twitch.tv")
        token_url = ("/oauth2/token?client_id={}"
                                   "&client_secret={}"
                                   "&code={}"
                                   "&grant_type=authorization_code"
                                   "&redirect_uri={}").format(self.client_id, self.client_secret, self.oauth_code, "http://localhost")
        token_response = oauth_client.make_request(token_url, type="post")
        if token_response.status_code != 200:
            print("ERROR: invalid status getting access token")
            pdb.set_trace()

        token_response = token_response.json()
        self.access_token = token_response['access_token']
        self.refresh_token = token_response['refresh_token']

        return (self.access_token, self.refresh_token)

# Test the authentication flow
if __name__ == "__main__":
    twitch_client = TwitchClient("******************", "*************************",None)
    oauth_code = twitch_client.init()