import base64
import requests
import datetime

client_id = "ceb26cec40f4432b807c40a0aeef6e4a"
client_secret = "d885f86f83074d1d9d0ec855558b7c2f"

client_creds = f"{client_id}:{client_secret}"

client_creds_b64 = base64.b64encode(client_creds.encode())
response_type = "code"

token_url = "https://accounts.spotify.com/api/token"
method = "POST"

token_data = {
    "grant_type":"client_credentials"
}
token_header = {
    "Authorization":f"Basic {client_creds_b64.decode()}" #Basic <base64 encoded client_id:client_secret>
}




r = requests.post(token_url, data=token_data, headers=token_header)

token_response_data = r.json()

now = datetime.datetime.now()
access_token = token_response_data['authorize']
expires_in = token_response_data['expires_in']
expires = now + datetime.timedelta(seconds=expires_in)
did_expire = expires < now