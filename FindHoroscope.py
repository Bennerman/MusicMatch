import json
import requests

r = requests.get(url="http://horoscope-api.herokuapp.com/horoscope/today/Libra")

data = r.json()

print(data)

#key = "ef5ff5341ab06ee976da5fa46ee2c6420c3c6e55105b79e37e032cd2953e8a0e"
#base_url = "https://api.prokerala.com/dashboard/home"



print("Hello casey and alex")

print("we should smoke in the next 2 hours")