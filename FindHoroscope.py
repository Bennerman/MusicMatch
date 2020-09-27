
import requests
import json 


params = (
('sign', 'gemini'),
('day', 'today'),
)

r = requests.post('https://aztro.sameerkumar.website/', params=params)

data = r.json()

print(data)
