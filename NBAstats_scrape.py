from bs4 import BeautifulSoup
import requests
import csv

# TODO: ADD THE CURRENT DATE REQUESTED AS A SUFFIX TO THE FILE NAME
player_data = "Player_Data.csv"
player_data_headers = ['Name', 'Team', 'PER', 'Minutes Played']

with open(player_data, 'wb+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = player_data_headers, delimiter = ',')
    writer.writeheader()
    writer = csv.writer(csv_file)
    url = 'https://www.basketball-reference.com/leagues/NBA_2020_advanced.html'
    r  = requests.get(url)

    soup = BeautifulSoup(data, "html.parser")

    table = soup.find('tbody')

    for entry in table.find_all('tr'):
        row = []
        for cell in table.find_all('td'):
            if cell.attrs['data-stat'] == 'player':
                name = cell.find('a').text.strip()
                print(name)




