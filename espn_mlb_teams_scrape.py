import urllib.request
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

url = 'https://www.espn.com/mlb/teams'

html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, features='lxml')
links = soup.findAll("a", href=True)

team_links = set()
for link in links:
    if re.search(r'mlb/team/_/name/',link['href']):
        team_links.add('espn.com' + link['href'])

teams = []
for team_link in team_links:
    team_id = re.sub(r'.*/name/([^/]*)/.*', r'\1', team_link)
    teams.append((team_link, team_id))

df = pd.DataFrame(teams, columns=['link', 'id']).sort_values('id')
df.to_csv('data/mlb_teams.csv', index=False)
