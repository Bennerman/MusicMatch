import base64
import requests
import datetime

from urllib.parse import urlencode

#######################
# Authorization Setup #
#######################

'''
client_creds = f"{client_id}:{client_secret}"

client_creds_b64 = base64.b64encode(client_creds.encode())
response_type = "code"

token_url = "https://accounts.spotify.com/api/token"
method = "POST"

token_data = {
    "grant_type": "client_credentials"
}
token_header = {
    # Basic <base64 encoded client_id:client_secret>
    "Authorization": f"Basic {client_creds_b64.decode()}"
}


r = requests.post(token_url, data=token_data, headers=token_header)
valid_request = r.status_code in range(
    200, 299)  # checks whether request is valid

if valid_request:

    token_response_data = r.json()

    now = datetime.datetime.now()

    access_token = token_response_data['access_token']
    expires_in = token_response_data['expires_in']
    expires = now + datetime.timedelta(seconds=expires_in)
    did_expire = expires < now

'''

client_id = "ceb26cec40f4432b807c40a0aeef6e4a"
client_secret = "d885f86f83074d1d9d0ec855558b7c2f"

class SpotifyAPI(object):  # pass object?
 

    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        '''
        Returns a b64 enocoded string
        '''

        client_id = self.client_id
        client_secret = self.client_secret

        if client_secret == None or client_id == None:
            raise Exception("Could not authenticate client")

        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())

        return client_creds_b64

    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }
    
    #Returns true if authorized, false otherwise
    def perfom_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_header)
        

        if r.status_code not in range(200, 299):
            return False

        data = r.json()

        now = datetime.datetime.now()

        access_token = data['access_token']
        self.access_token = access_token
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
            
        return True

    def get_access_token(self):
        auth = self.perfom_auth()
        if not auth:
            raise Exception("Authentication failed")
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perfom_auth()
        elif token == None:
            self.perfom_auth()
            return self.get_access_token()
        return token


    def search(self, query, search_type="artist"):
        access_token = self.get_access_token()

        headers = {
            "Authorization": "Bearer " + access_token
        }

        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q":query, "type": search_type})
        lookup_url = f"{endpoint}?{data}"

        r = requests.get(lookup_url, headers=headers)
        print(r.status_code)
        if r.status_code in range(200, 299):
            return r.json()
        return r.json()

    

    # def get_album(self, _id):
        
    #     pass
    
    # def get_artist(self, _id):
    #     endpoint = "https://api.spotify.com/"
    #     data = 	urlencode(f"{base_url}/v1/artists/{_id}")


    #     pass


spotify = SpotifyAPI(client_id, client_secret)

spotify.perfom_auth()
#access_token = spotify.access_token


#use bearer instead of basic


# headers = {
#     "Authorization": "Bearer " + access_token
# }

# print(headers["Authorization"])
# endpoint = "https://api.spotify.com/v1/search"

# data = urlencode({"q":"Replay", "type": "track"})

# lookup_url = f"{endpoint}?{data}"

# r = requests.get(lookup_url, headers=headers)

# print(r.text)
# print(r.status_code)

print(spotify.search("Travis Scott", search_type="artist"))

'''
IMPORTANT

valence	float	A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. 
                Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while 
                tracks with low valence sound more negative (e.g. sad, depressed, angry).

popularity	int	The popularity of the track. The value will be between 0 and 100, with 100 being the most popular. 
                The popularity is calculated by algorithm and is based, in the most part, on the total number of plays 
                the track has had and how recent those plays are. Note: When applying track relinking via the market parameter, 
                it is expected to find relinked tracks with popularities that do not match min_*, max_*and target_* popularities. 
                These relinked tracks are accurate replacements for unplayable tracks with the expected popularity scores. 

energy	float	Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. 
                Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, 
                while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute 
                include dynamic range, perceived loudness, timbre, onset rate, and general entropy.

danceability	float	Danceability describes how suitable a track is for dancing based on a combination of musical elements including 
                        tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.

limit           Optional. The target size of the list of recommended tracks. 
                For seeds with unusually small pools or when highly restrictive filtering is applied, 
                it may be impossible to generate the requested number of recommended tracks. 
                Debugging information for such cases is available in the response. Default: 20. Minimum: 1. Maximum: 100.