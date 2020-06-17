''' 
A web scraper used to scrape the listed site for basketball data. 
@author: William Zhang, Timothy Wu
'''
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime

# Create a CSV file with the current DateTime in the name
current_time = datetime.now()
dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
player_data = "Player_Data.csv"

# The column titles for the data we're collecting 
player_data_headers = ['Name', 'Team', 'Minutes Played', 'PER']

# Change this when the year/season changes 
curr_year = 2020
# Team abbreviations
team_abbreviations = ['TOR', 'BOS', 'PHI', 'BRK', 'NYK', 'MIL', 'IND', 'CHI', 'DET', 'CLE', 'MIA', 'ORL', 'WAS', 'CHO', 'ATL','DEN','UTA', 'OKC', 'POR', 'MIN', 'LAL', 'LAC','SAC','PHO','GSW','HOU', 'DAL', 'MEM','NOP','SAS']
player_team_headers = ['Name', 'Team', 'Position'] 


url = 'https://www.basketball-reference.com/leagues/NBA_2020_advanced.html'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "html.parser")

table = soup.find('tbody')
all_rows = []
for entry in table.find_all('tr'):
    row = []
    for cell in entry.find_all('td'):
        if cell.attrs['data-stat'] == 'player':
            name = cell.find('a').text.strip()
            row.append(name)
        elif cell.attrs['data-stat'] == 'team_id':
            team = ""
            if cell.find('a') == None: 
                team = cell.text.strip()
            else: 
                team = cell.find('a').text.strip()
            row.append(team)
        elif cell.attrs['data-stat'] == 'mp':
            mp = cell.text.strip()
            row.append(mp)
        elif cell.attrs['data-stat'] == 'per':
            per = cell.text.strip()
            row.append(per)
    all_rows.append(row)


df = pd.DataFrame(data=all_rows,  columns=player_data_headers)
df.set_index(['Name', 'Team'], drop = True, inplace = True)
print(df.head())
df.to_csv('Player_Data_pandas.csv', encoding = 'utf-8')
        
for team_name in team_abbreviations:
    team_data = team_name + ".csv"
     

    url = 'https://www.basketball-reference.com/teams/' + team_name + '/' + str(curr_year) + '.html'
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    table = soup.find('tbody')
    all_rows = []
    for entry in table.find_all('tr'):
        row = []
        for cell in entry.find_all('td'):
            if cell.attrs['data-stat'] == 'player':
                name = cell.find('a').text.strip()
                row.append(name)
                row.append(team_name)
            elif cell.attrs['data-stat'] == 'pos':
                pos = cell.text.strip()
                row.append(pos)
        all_rows.append(row)
    df = pd.DataFrame(data=all_rows,  columns=player_team_headers)
    df.set_index(['Name', 'Team'], drop = True, inplace = True)
    print(df.head())
    df.to_csv(team_data, encoding = 'utf-8')
    
            

