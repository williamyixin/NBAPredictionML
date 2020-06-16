from bs4 import BeautifulSoup
import requests
import csv

# TODO: ADD THE CURRENT DATE REQUESTED AS A SUFFIX TO THE FILE NAME
player_data = "Player_Data.csv"
player_data_headers = ['Name', 'Team', 'Minutes Played', 'PER']

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
        




