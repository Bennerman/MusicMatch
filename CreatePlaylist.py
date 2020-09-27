import base64
import requests
import datetime

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
            raise Exception("You need to set client_id and client_secret")

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

client = SpotifyAPI(client_id, client_secret)
print(client.perfom_auth())
