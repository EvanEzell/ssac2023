import urllib.request
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

teams_df = pd.read_csv('data/mlb_teams.csv')

season = '2021'

prefix = 'https://www.espn.com/mlb/team/schedule/_/name/'
suffix = '/season/' + season + '/seasontype/2/half/'

urls = []
for index, row in teams_df.iterrows():
    team = row['id']
    url = prefix + team + suffix
    for season_half in ['1', '2']:
        urls.append(url + season_half)

game_urls = set()
for url in urls:
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features='lxml')
    links = soup.findAll("a", href=True)
    for link in links:
        if re.search(r'gameId', link['href']):
            game_urls.add(link['href'])

game_ids = []
for game_url in game_urls:
    game_id = re.sub(r'.*/(.*)$', r'\1', game_url)
    game_ids.append(game_id)

df = pd.DataFrame(list(zip(game_urls, game_ids)), columns = ['link', 'id'])
df.to_csv('data/mlb_games.csv', index=False)
