import NBAstats_scrape
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime
import numpy as np

'''
Generates the training data.
'''
#years to scrape
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

#current minutes threshold for new players/new season, but we could look to change this to some other value
minutes_threshold = 50

#features of the final training data set
features = ['FG/MP_Home_Starter', 'FGA/MP_Home_Starter', '3P/MP_Home_Starter', '3PA/MP_Home_Starter', 
            'FT/MP_Home_Starter', 'FTA/MP_Home_Starter', 'ORB/MP_Home_Starter', 'DRB/MP_Home_Starter', 
            'AST/MP_Home_Starter', 'STL/MP_Home_Starter', 'BLK/MP_Home_Starter', 'TOV/MP_Home_Starter', 
            'PF/MP_Home_Starter', 'PTS/MP_Home_Starter', 'FG/MP_Home_Other', 'FGA/MP_Home_Other', '3P/MP_Home_Other', 
            '3PA/MP_Home_Other', 'FT/MP_Home_Other', 'FTA/MP_Home_Other', 'ORB/MP_Home_Other', 'DRB/MP_Home_Other', 
            'AST/MP_Home_Other', 'STL/MP_Home_Other', 'BLK/MP_Home_Other', 'TOV/MP_Home_Other', 'PF/MP_Home_Other', 
            'PTS/MP_Home_Other', 'FG/MP_Away_Starter', 'FGA/MP_Away_Starter', '3P/MP_Away_Starter', '3PA/MP_Away_Starter', 
            'FT/MP_Away_Starter', 'FTA/MP_Away_Starter', 'ORB/MP_Away_Starter', 'DRB/MP_Away_Starter', 'AST/MP_Away_Starter', 
            'STL/MP_Away_Starter', 'BLK/MP_Away_Starter', 'TOV/MP_Away_Starter', 'PF/MP_Away_Starter', 'PTS/MP_Away_Starter', 
            'FG/MP_Away_Other', 'FGA/MP_Away_Other', '3P/MP_Away_Other', '3PA/MP_Away_Other', 'FT/MP_Away_Other', 'FTA/MP_Away_Other', 
            'ORB/MP_Away_Other', 'DRB/MP_Away_Other', 'AST/MP_Away_Other', 'STL/MP_Away_Other', 'BLK/MP_Away_Other', 'TOV/MP_Away_Other', 
            'PF/MP_Away_Other', 'PTS/MP_Away_Other', 'Homewin', 'GameID']

#method that takes the row of data and reorients it and removes the name from it
def removename(row):
    temp = row.reset_index(drop=True)
    l = list(temp.values)
    df = pd.DataFrame(data=l, index=player_stats[1:])
    return df

#reorients the data and divides it
def fixdataforjoin(data):
    data = data.transpose()
    data = data.div(data['mp'] / 60, axis='index')
    data = data.drop("mp", axis=1) 
    return data

#set the values for default player, can look to change rn it is set to 0s
def default(player_name):
    row = pd.DataFrame(np.zeros((1,len(player_stats))), columns=player_stats)
    row['player'] = player_name
    row.set_index('player', inplace=True)
    return row

#beef of scraper: takes data and updates the team dictionary as well as the starter and other dataframes for corresponding teams
def datamanip(team, side, starter, other):
    if table.attrs['id'] == 'box-' + team + '-game-basic':
        #keep track of who is starter and who is not
        startercounter = 0
        for player_row in table_body.find_all('tr'):
            #skip the bar separating starters and other players in html
            if 'class' in player_row.attrs and player_row.attrs['class'] == ['thead']:
                continue
            startercounter += 1
            player_name = player_row.find('a').text.strip()
            
            # check if player is already in team dataframe
            if player_name in team_dict[team].index:
                row = team_dict[team].loc[player_name]
                
                # if in dataframe, check if he has more than minutes threshold 
                if row['mp'] < minutes_threshold:
                    # if not, check if he was in prev season
                    if player_name in previous_season_player_data.index: 
                        #use previous season
                        row = previous_season_player_data.loc[player_name]
                    else: 
                        #if not, use default values (to be determined)
                        row = default(player_name)
            else: # if not, check if he was in prev season
                if player_name in previous_season_player_data.index: 
                    #use previous season
                    row = previous_season_player_data.loc[player_name]
                else: 
                    #if not, use default values (to be determined)
                    row = default(player_name)
            #convert row to be able to add
            row = row.apply(pd.to_numeric)
            #convert minutes to seconds
            row['mp'] = row['mp'] * 60
            #add to starter if starter otherwise add to other
            if startercounter < 7:
                df = removename(row)
                starter = starter.add(df, fill_value=0, axis=1)
            else:
                df = removename(row)
                other = other.add(df, fill_value=0, axis=1)
            tds = player_row.find_all('td')
            #take all players that played (skips players that did not play/did not dress/suspended)
            temp = [cell.text.strip() for cell in tds if cell.attrs['data-stat'] != 'reason']
            #skip percentage based stats
            playerdata = temp[0:3] + temp[4:6] + temp[7:9] + temp[10:12] + temp[13:19]
            #as long as it is not empty
            if temp:
                #convert time to seconds
                time = playerdata[0].split(":")
                minutes = int(time[0])
                seconds = int(time[1])
                playerdata[0] = minutes * 60.0 + seconds
                playerdata[0] = playerdata[0] / 60.0
                playerdata.insert(0, player_name)
                #reorient the data
                playerdata = pd.DataFrame(data=playerdata)
                playerdata = playerdata.transpose()
                playerdata.columns = player_stats
                playerdata.set_index("player", inplace=True)
                #append to team dictionary if it is not there or add it
                if not player_name in team_dict[team].index:
                    team_dict[team] = team_dict[team].append(playerdata)
                else:
                    playerdata = playerdata.apply(pd.to_numeric)
                    temp = team_dict[team].loc[player_name].apply(pd.to_numeric)
                    temp = temp + playerdata
                    temp = temp.iloc[0]
                    l = temp.to_list()
                    team_dict[team].loc[player_name] = l
        table_foot = table.find('tfoot')
        tr = table_foot.find('tr')
        tds = tr.find_all('td')
        score = 0
        #get scores of each team
        if side == 'away':
            score = int(tds[18].text.strip())
        else:
            score = int(tds[18].text.strip())
        return starter, other, score
#training data dataframe
trainingdata = pd.DataFrame(columns=features, index=['GameID'])
#print when scraping started
print("started", end="")
print(datetime.datetime.now())
for year in years: 
#if True:
    #year = 2018
    print(f"Currently Scraping {year}")
    #Get basic info for NBA teams in this current year
    NBAstats_scrape.generate_previous_season(year)
    game_links = NBAstats_scrape.get_game_links(year)
    team_abbreviations = NBAstats_scrape.get_team_names(year)
    previous_season_player_data = pd.read_csv('data/' + str(year - 1) + '_end_of_season_player_summary.csv', encoding = 'utf-8')
    previous_season_player_data.set_index('player', inplace = True)
    print(previous_season_player_data.head())
    # Data Structure Initialization
    player_stats = ['player', 'mp', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB','DRB','AST','STL','BLK','TOV','PF','PTS']
    team_dict = {}
    
    for team in team_abbreviations:
        team_dict[team] = pd.DataFrame(columns = player_stats) 
        team_dict[team].set_index('player', inplace = True)

    for link in game_links: 
    #if True:
        #link = "https://www.basketball-reference.com/boxscores/201710170CLE.html"
        r = requests.get(link)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        home_team = link[-8:-5]
        away_team = ''
        home_score = 0
        away_score = 0
        
        # Gets the away team and score
        for div in soup.find_all('div'):
            if 'class' in div.attrs and div.attrs['class'] == ['scorebox']: 
                for a_tag in div.find_all('a'): 
                    if re.search('\/teams\/[A-Z]{3}\/[0-9]{4}.html', a_tag.attrs['href']):
                        away_team = a_tag.attrs['href'][7:10]
                        break
                break 

        #initialize dataframes for starter and other for both teams
        Home_Starter = pd.DataFrame(index=player_stats[1:])
        Home_Other = pd.DataFrame(index=player_stats[1:])
        Away_Starter = pd.DataFrame(index=player_stats[1:])
        Away_Other = pd.DataFrame(index=player_stats[1:])
        print(f"{away_team} vs {home_team} {year}")

        for table in soup.find_all('table'):
            table_body = table.find('tbody')

            # if this is the table for the away team
            if table.attrs['id'] == 'box-' + away_team + '-game-basic':
                Away_Starter, Away_Other, away_score = datamanip(away_team, "away", Away_Starter, Away_Other)
                            
            #home team
            elif table.attrs['id'] == 'box-' + home_team + '-game-basic':
                Home_Starter, Home_Other, home_score = datamanip(home_team, "home", Home_Starter, Home_Other)
        
        #fix data for the join
        Home_Starter = fixdataforjoin(Home_Starter)
        Home_Other = fixdataforjoin(Home_Other)
        Away_Starter = fixdataforjoin(Away_Starter)
        Away_Other = fixdataforjoin(Away_Other)

        #fix the column names for each
        Home_Starter = Home_Starter.add_suffix('/MP_Home_Starter')
        Home_Other = Home_Other.add_suffix('/MP_Home_Other')
        Away_Starter = Away_Starter.add_suffix('/MP_Away_Starter')
        Away_Other = Away_Other.add_suffix('/MP_Away_Other')
        
        #join them together
        row = Home_Starter.join(Home_Other)
        row = row.join(Away_Starter)
        row = row.join(Away_Other)

        #determines who wins
        if home_score > away_score:
            row['Homewin'] = 1
        else:
            row['Homewin'] = 0
        #set the game id
        row['GameID'] = f"{away_team} vs {home_team} {year}"
        row.set_index('GameID', inplace=True)
        #for some reason row becomes a n by n dataframe instead of n by 1 so i take the first row could be something to look into
        trainingdata = trainingdata.append(row.iloc[0])
        print(f"{away_team} vs {home_team} {year} done")
    trainingdata.to_csv('trainingdata.csv', encoding='utf-8')
    print(f"trainingdata {year} done")

#print end time (4-5 hours atm)
print("finished", end="")
print(datetime.datetime.now())






        


                    