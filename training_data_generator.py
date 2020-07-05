import NBAstats_scrape
import pandas as pd
import requests
from bs4 import BeautifulSoup

'''
Generates the training data.
'''

years = [2018]

minutes_threshold = 100

for year in years: 
    #Get basic info for NBA teams in this current year
    NBAstats_scrape.generate_previous_season(year)
    game_links = NBAstats_scrape.get_game_links(year)
    team_abbreviations = NBAstats_scrape.get_team_names(year)
    
    # Data Structure Initialization
    player_stats = ['player', 'mp', 'fg', 'fga', 'three_p', 'three_p_a', 'ft', 'fta', 'orb','drb','trb','ast','stl','blk','tov','pf','pts']
    team_dict = {}
    team_paces = {}
    league_totals = {'lg_AST','lg_FG','lg_FT', 'lg_PTS', 'lg_FGA', 'lg_ORB', 'lg_TOV', 'lg_FTA', 'lg_PF'}
    
    
    for team in team_abbreviations:
        team_dict[team] = pd.DataFrame(columns = player_stats) 
        # First element is sum of all paces, second element is number of games played
        team_paces[team] = [0, 0]

        
    for link in game_links: 
        r = requests.get(link)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        home_team = link[-8:-5]
        away_team = ''
        for div in soup.find_all('div'):
            if 'id' in div.attrs and div.attrs['id'] == 'all_four_factors': 
                for row in div.find_all('tr'):
                    print(row)
        '''
        for table in soup.find_all('table'):
            print(table.attrs['id'])
            if 'id' in table.attrs and table.attrs['id'] == 'four_factors':
                body = table.find('tbody')
                away_team = body.find('a').text
                print(home_team + away_team)
'''

        break;

                    