''' 
A web scraper used to scrape the listed site for basketball data. 
@author: William Zhang, Timothy Wu
'''

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
player_team_headers = ['Name', 'Team'] 

with open(player_data, mode = 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(player_data_headers)
    

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
                name = cell.find('a').text.strip().encode('utf-8')
                row.append(name)
            elif cell.attrs['data-stat'] == 'team_id':
                team = ""
                if cell.find('a') == None: 
                    team = cell.text.strip().encode('utf-8')
                else: 
                    team = cell.find('a').text.strip().encode('utf-8')
                row.append(team)
            elif cell.attrs['data-stat'] == 'mp':
                mp = cell.text.strip().encode('utf-8')
                row.append(mp)
            elif cell.attrs['data-stat'] == 'per':
                per = cell.text.strip().encode('utf-8')
                row.append(per)
        all_rows.append(row)

    print(all_rows)
    writer.writerows(all_rows)
            
for team_name in team_abbreviations:
    team_data = team_name + ".csv"

    with open(team_data, mode = 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(player_team_headers)
        

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
                    name = cell.find('a').text.strip().encode('utf-8')
                    row.append(name)
                    break;
            row.append(team_name.encode('utf-8'))
            all_rows.append(row)

        print(all_rows)
        writer.writerows(all_rows)
            

