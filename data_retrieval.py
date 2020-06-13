import json
import requests

api_token = 'your_api_token'
api_url_base = 'https://api.sportsdata.io/v3/nba/scores/xml/TeamSeasonStats/2018'
key = '41fe58ffbb3a4021ad2bc8e21c81a10b'
params =dict(Ocp-Apim-Subscription-Key='41fe58ffbb3a4021ad2bc8e21c81a10b')

data = requests.get(api_url_base, params = params)

print(type(data))