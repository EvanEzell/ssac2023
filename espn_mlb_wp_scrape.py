import urllib.request
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from alive_progress import alive_bar
import time


def get_wp(event_id, attempts = 3, sleep = 3):
    url = ('http://site.api.espn.com/apis/site/v2/sports/' +
           'baseball/mlb/summary?event=' + str(event_id))
    for attempt in range(1, attempts + 1):
        try:
            json_text = urllib.request.urlopen(url).read()
            break
        except Exception as e:
            print('Failed to scrape game: ' + str(event_id))
            print('Request error: ' + str(e))
            if attempt != attempts:
                time.sleep(sleep)
                print('Trying again...')
            else:
                return 'RequestError'
    data_dict = json.loads(json_text)
    if 'winprobability' not in data_dict:
        return 'NA'
    wp = data_dict['winprobability']
    timeseries = []
    for el in wp:
        timeseries.append(el['homeWinPercentage'])
    return timeseries

games_df = pd.read_csv('data/mlb_games.csv')

win_probs = []
with alive_bar(len(games_df)) as bar:
    for index, row in games_df.iterrows():
        event_id = row['id']
        win_probs.append((event_id, get_wp(event_id)))
        bar()

rows = []
for event_id, win_prob in win_probs:
    if not isinstance(win_prob, list):
        rows.append((event_id, 'NA', win_prob))
        continue
    for play, perc in enumerate(win_prob):
        rows.append((event_id, play, perc))

df = pd.DataFrame(rows, columns = ['game_id', 'play_no', 'wp'])
df.to_csv('data/mlb_win_probabilities.csv', index=False)
