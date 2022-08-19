import requests

base_url = 'https://pds-wordie.herokuapp.com'
player_key = 'RSFTSQY'

response = requests.get(f'{base_url}/api/games/')

games = response.json()['games']
for el in games:
    print(el)
print(len(games))