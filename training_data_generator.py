import NBAstats_scrape
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

'''
Generates the training data.
'''

years = [2018]

minutes_threshold = 50

for year in years: 
    #Get basic info for NBA teams in this current year
    NBAstats_scrape.generate_previous_season(year)
    game_links = NBAstats_scrape.get_game_links(year)
    team_abbreviations = NBAstats_scrape.get_team_names(year)
    print(game_links[0])
    previous_season_player_data = pd.read_csv('data/' + str(year - 1) + '_end_of_season_player_summary.csv', encoding = 'utf-8')
    previous_season_player_data.set_index('player', inplace = True)
    print(previous_season_player_data.head())
    # Data Structure Initialization
    player_stats = ['player', 'mp', 'fg', 'fga', 'three_p', 'three_p_a', 'ft', 'fta', 'orb','drb','ast','stl','blk','tov','pf','pts']
    team_dict = {}
    
    for team in team_abbreviations:
        team_dict[team] = pd.DataFrame(columns = player_stats) 
        team_dict[team].set_index('player', inplace = True)


        
    for link in game_links: 
        r = requests.get(link)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        home_team = link[-8:-5]
        away_team = ''
        n = 0
        
        # Gets the away team
        for div in soup.find_all('div'):
            if 'class' in div.attrs and div.attrs['class'] == ['scorebox']: 
                for a_tag in div.find_all('a'): 
                    if re.search('\/teams\/[A-Z]{3}\/[0-9]{4}.html', a_tag.attrs['href']):
                        away_team = a_tag.attrs['href'][7:10]
                        break; 
                break;
                
        home_data = team_dict[home_team]
        away_data = team_dict[away_team]
    
        for table in soup.find_all('table'):
            table_body = table.find('tbody')

            # if this is the table for the away team
            if table.attrs['id'] == 'box-' + away_team + '-game-basic':
                for player_row in table_body.find_all('tr'):
                    player_name = player_row.find('a').text.strip()
                    
                    # check if player is already in team dataframe
                    if player_name in away_data.index:
                        row = data.loc[player_name]
                        
                        # if in dataframe, check if he has more than 100 min 
                        if row['mp'] > minutes_threshold:
                            a = 0# if so, use current data
                        else:
                            a = 0 
                            # if not, check if he was in prev season
                            if player_name in previous_season_player_data.index: 
                                # if so, use prev season data to calc PER\
                            else: 
                                #if not, use default values (to be determined)
                    else: # if not, check if he was in prev season
                        if player_name in previous_season_player_data.index: 
                                # if so, use prev season data to calc PER\
                        else: 
                            #if not, use default values (to be determined)
                            


            elif table.attrs['id'] == 'box-' + home_team + 'game-basic':
                a = 0
                


        break;

                    