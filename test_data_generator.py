import NBAstats_scrape
import pandas as pd
import numpy as np
import xgboost as xgb
import os

minutes_threshold = 50
year = 2020
player_stats = ['player', 'mp', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB','DRB','AST','STL','BLK','TOV','PF','PTS']

def get_input():
    f = open('input/HOU_VS_SAS.in', "r",encoding='utf-8')
    away_starter = []
    away_other = []
    home_starter = []
    home_other = []
    away_team = ''
    home_team = ''
    home = True
    starter_count = 0
    for s in f: 
        s = s.strip()
        if s[0:4] == 'Home': 
            home_team = s[6:9]
        elif s[0:4] == 'Away':
            away_team = s[6:9]
            home = False
            starter_count = 0
        elif home:
            if (starter_count < 5): 
                home_starter.append(s)
                starter_count += 1
            else: 
                home_other.append(s)
        elif not home: 
            if starter_count < 5: 
                away_starter.append(s)
                starter_count += 1
            else: 
                away_other.append(s)

    return [home_team, away_team, home_starter, home_other, away_starter, away_other]



#method that takes the row of data and reorients it and removes the name from it
def removename(row):
    temp = row.reset_index(drop=True)
    l = list(temp.values)
    df = pd.DataFrame(data=l, index=player_stats[1:])
    return df

#reorients the data and divides it
def fixdataforjoin(data):
    data = data.transpose()
    data = data.div(data['mp'], axis='index')
    data = data.drop("mp", axis=1) 
    return data

#set the values for default player, can look to change rn it is set to 0s
def default(player_name):
    '''
    l = default_generator.get_average(year)
    row = pd.DataFrame(data=l)
    row = row.transpose()
    row.columns = player_stats
    row['player'] = player_name
    row.set_index('player', inplace=True)
    '''
    row = pd.DataFrame({'player': player_name, 'mp': 0, 'FG': 0, 'FGA': 0, '3P': 0, '3PA': 0, 'FT': 0, 'FTA': 0, 
                        'ORB': 0,'DRB': 0,'AST': 0,'STL': 0,'BLK': 0,'TOV': 0,'PF': 0,'PTS': 0}, index=[0])
    row.set_index('player', inplace=True)
    return row

def data(starter, other, starterlist, otherlist, currentdata, previousdata):
    for player_name in starterlist:
        if player_name in currentdata.index:
            row = currentdata.loc[player_name]

            if row['mp'] < minutes_threshold:
                if player_name in previousdata.index:
                    row = previousdata.loc[player_name]
                else:
                    row = default(player_name)
        else:
            if player_name in previousdata.index:
                    row = previousdata.loc[player_name]
            else:
                row = default(player_name)
        row = row.apply(pd.to_numeric)
        #row['mp'] = row['mp'] * 60
        df = removename(row)
        starter = starter.add(df, fill_value=0, axis=1)
    for player_name in otherlist:
        if player_name in currentdata.index:
            otherrow = currentdata.loc[player_name]

            if otherrow['mp'] < minutes_threshold:
                if player_name in previousdata.index:
                    otherrow = previousdata.loc[player_name]
                else:
                    otherrow = default(player_name)
        else:
            if player_name in previousdata.index:
                otherrow = previousdata.loc[player_name]
            else:
                otherrow = default(player_name)
        otherrow = otherrow.apply(pd.to_numeric)
        #otherrow['mp'] = otherrow['mp'] * 60
        df = removename(otherrow)
        other = other.add(df, fill_value=0, axis=1)
    return starter, other

def generate_row(home_starters, home_others, away_starters, away_others, home_team, away_team):
    NBAstats_scrape.generate_previous_season(year+1)
    current_season_player_data = pd.read_csv('data/' + str(year) + '_end_of_season_player_summary.csv', encoding='utf-8')
    current_season_player_data.set_index('player', inplace=True)
    previous_season_player_data = pd.read_csv('data/' + str(year - 1) + '_end_of_season_player_summary.csv', encoding = 'utf-8')
    previous_season_player_data.set_index('player', inplace = True)
    

    Home_Starter = pd.DataFrame(index=player_stats[1:])
    Home_Other = pd.DataFrame(index=player_stats[1:])
    Away_Starter = pd.DataFrame(index=player_stats[1:])
    Away_Other = pd.DataFrame(index=player_stats[1:])

    Away_Starter, Away_Other = data(Away_Starter, Away_Other, away_starters, away_others, current_season_player_data, previous_season_player_data)
    Home_Starter, Home_Other = data(Home_Starter, Home_Other, home_starters, home_others, current_season_player_data, previous_season_player_data)

    Home_Starter = fixdataforjoin(Home_Starter)
    Home_Other = fixdataforjoin(Home_Other)
    Away_Starter = fixdataforjoin(Away_Starter)
    Away_Other = fixdataforjoin(Away_Other)

    Home_Starter = Home_Starter.add_suffix('/MP_Home_Starter')
    Home_Other = Home_Other.add_suffix('/MP_Home_Other')
    Away_Starter = Away_Starter.add_suffix('/MP_Away_Starter')
    Away_Other = Away_Other.add_suffix('/MP_Away_Other')

    row = Home_Starter.join(Home_Other)
    row = row.join(Away_Starter)
    row = row.join(Away_Other)
    row['GameID'] = f"{away_team} vs {home_team} {year}"
    row.set_index('GameID', inplace=True, drop=True)
    row.dropna(inplace=True)
    return row

def prediction(model, row, hometeam, awayteam):
    data = row.reset_index(drop=True)
    prediction = model.predict(data)
    winpercentage = model.predict_proba(data)[:,1]
    '''
    #uncomment if not 2020
    if prediction == 1:
        print(f"{hometeam} will win with a {winpercentage} % chance")
    else:
        print(f"{awayteam} will win with a {1-winpercentage} % chance")
    '''
    return winpercentage
    
inputs = get_input()
homestarter = inputs[2]
homeother = inputs[3]
awaystarter = inputs[4]
awayother = inputs[5]
hometeam = inputs[0]
awayteam = inputs[1]
print(awaystarter)
print(awayother)
print(homestarter)
print(homeother)
row = generate_row(homestarter, homeother, awaystarter, awayother, hometeam, awayteam)
model = xgb.XGBClassifier()
model.load_model('FULLNBAMODEL2010-2020test.model')
homewinpercentage = prediction(model, row, hometeam, awayteam)

#for 2020 season
tempsecondrow = generate_row(awaystarter, awayother, homestarter, homeother, awayteam, hometeam)
secondhomewinpercentage = prediction(model, tempsecondrow, awayteam, hometeam)

print(f"{hometeam} at home win percentage: {homewinpercentage}")
print(f"{awayteam} at home win percentage: {secondhomewinpercentage}")
homewinaverage = (homewinpercentage + (1 - secondhomewinpercentage)) / 2.0
if homewinaverage > 0.5:
    print(f"{hometeam} will win with a {homewinaverage} % chance")
else:
    print(f"{awayteam} will win with a {1-homewinaverage} % chance")

os.getcwd()
if not os.path.exists('GameRows'):
    os.mkdir('GameRows')

row.to_csv(f"GameRows/{awayteam}@{hometeam}_{year}.csv", encoding='utf-8')




    