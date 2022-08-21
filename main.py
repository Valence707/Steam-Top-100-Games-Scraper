import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

url = 'https://store.steampowered.com/stats/'
headers = {'Accept-Language': 'en-US, en;q=0.5'}

utc_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
response = requests.get(url, headers)
soup = BeautifulSoup(response.text, 'html.parser')
detailStats = soup.find(id='detailStats')

current_players = []
peak_today = []
games = []

rows = detailStats.find_all('tr', class_='player_count_row')

for row in rows:
    current_players.append(row.find_all('span')[0].text if row.find_all('span')[0] else '')
    peak_today.append(row.find_all('span')[1].text if row.find_all('span')[1] else '')
    games.append(row.a.text if row.a else '')

top100 = pd.DataFrame({
    'game': games,
    'current_players': current_players,
    'peak_today': peak_today
})

top100['current_players'] = top100['current_players'].str.replace(',', '').astype(int, errors='ignore')
top100['peak_today'] = top100['peak_today'].str.replace(',', '').astype(int, errors='ignore')

top100.to_csv(F'steam_top_100_games_{utc_date}.csv')