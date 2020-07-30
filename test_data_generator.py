import NBAstats_scrape
import pandas as pd
import numpy as np
import xgboost as xgb

minutes_threshold = 50
year = 2020
player_stats = ['player', 'mp', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB','DRB','AST','STL','BLK','TOV','PF','PTS']
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
        row['mp'] = row['mp'] * 60
        df = removename(row)
        starter = starter.add(df, fill_value=0, axis=1)
    for player_name in otherlist:
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
        row['mp'] = row['mp'] * 60
        df = removename(row)
        other = other.add(df, fill_value=0, axis=1)
        return starter, other

def generate_row(home_starters, home_others, away_starters, away_others, home_team, away_team):
    #NBAstats_scrape.generate_previous_season(year+1)
    current_season_player_data = pd.read_csv('data/' + str(year) + '_end_of_season_player_summary.csv', encoding='utf-8')
    current_season_player_data.set_index('player', inplace=True)
    print(current_season_player_data.head())
    previous_season_player_data = pd.read_csv('data/' + str(year - 1) + '_end_of_season_player_summary.csv', encoding = 'utf-8')
    previous_season_player_data.set_index('player', inplace = True)
    print(previous_season_player_data.head())
    

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
    if prediction == 1:
        print(f"{hometeam} will win with a {winpercentage} % chance")
    else:
        print(f"{awayteam} will win with a {winpercentage} % chance")
    
'''
awaystarter = ["Jaylen Brown", "Kyrie Irving", "Jayson Tatum", "Al Horford", "Gordon Hayward"]
awayother = ["Marcus Smart", "Terry Rozier", "Aron Baynes", "Semi Ojeleye", "Shane Larkin", "Daniel Theis", "Abdel Nader"]
homestarter = ["Lebron James", "Jae Crowder", "Derrick Rose", "Dwyane Wade", "Kevin Love"]
homeother = ["J.R. Smith", "Tristan Thompson", "Jeff Green", "Iman Shumpert", "Kyle Korver", "Cedi Osman", "Channing Frye", "José Calderón"]
row = generate_row(homestarter, homeother, awaystarter, awayother, "CLE", "BOS")
model = xgb.XGBClassifier()
model.load_model("NBAMODEL2010-2020.model")

prediction(model, row)
'''




    