
import requests
import json 

#Parameters to pass to the api

params = (
('sign', 'gemini'),
('day', 'today'),
)

#request to website
r = requests.post('https://aztro.sameerkumar.website/', params=params)

data = r.json()

mood = data['mood']


print(mood)
