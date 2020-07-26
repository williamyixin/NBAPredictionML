''' 
A web scraper used to scrape the listed site for basketball data. 
@author: William Zhang, Timothy Wu
'''
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import re
from datetime import datetime

'''
Generates the end of season PER's for the previous season and puts it all into a csv
These stats will be used in place of stats for the current season 
When stats for the current season are insufficient.
'''
def generate_previous_season(curr_year):
    prev_year = curr_year - 1
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(prev_year) + '_totals.html'
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find('tbody')
    all_rows = []
    stats_we_want = ['player', 'mp', 'fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta', 'orb', 'drb', 'ast','stl','blk','tov','pf','pts']
    for entry in table.find_all('tr'):
        row = []
        for cell in entry.find_all('td'):
            if cell.attrs['data-stat'] == 'player':
                name = cell.find('a').text.strip()
                row.append(name)
            elif cell.attrs['data-stat'] in stats_we_want:
                stat = cell.text.strip()
                row.append(stat)
        if len(row) != 0 and (len(all_rows) == 0 or all_rows[-1][0] != row[0]):
            all_rows.append(row)
    df = pd.DataFrame(data=all_rows,  columns=stats_we_want)
    #df = df.append(pd.Series(0,index=df.columns), ignore_index=True)
    df.set_index(['player'], drop = True, inplace = True)
    df.to_csv('data/' + str(prev_year) + '_end_of_season_player_summary.csv', encoding = 'utf-8')
        
'''
Returns all the links to the box scores of games of a year in a list
'''
def get_game_links(year):
    months = []
    if year == 2020: 
        months = ['october', 'november', 'december', 'january', 'february', 'march']
    elif year == 2012:
        months = ['december', 'january', 'february', 'march', 'april', 'may', 'june']
    else: 
        months = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']
    links = []
    for month in months: 
        url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '_games-' + month + '.html'
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find('tbody')
        for entry in table.find_all('tr'):
            for cell in entry.find_all('td'):
                if cell.attrs['data-stat'] == 'box_score_text':
                    suffix = cell.find('a').attrs['href']
                    links.append('https://www.basketball-reference.com' + suffix)
    return links

'''
Returns a list of the team abbreviations given the year.
'''
def get_team_names(year):
    team_names = []
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    tables = 0
    for div in soup.find_all('div'):
        if ('class' in div.attrs) and div.attrs['class'] == 'standings_confs data_grid section_wrapper':
            tables = div
            break
    
    for link_tag in soup.find_all('a'):
        link = link_tag.attrs['href']
        if re.search('\/teams\/[A-Z]{3}\/[0-9]{4}.html', link):
            if not (link[7:10] in team_names):
                team_names.append(link[7:10])
    return team_names

'''
Returns the soup of link, given the link
'''
def get_soup(link):
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    return soup

'''# Create a CSV file with the current DateTime in the name
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
    
            

'''