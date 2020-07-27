import pandas as pd



def get_average(): 
    rookie_data = pd.read_csv('data/2019rookies.csv')
    rookie_data.drop(columns = ['Rk', 'G', 'Player', 'Debut', 'Age', 'Yrs', 'FG%', '3P%', 'FT%', 'MP.1', 'PTS.1', 'TRB.1', 'AST.1'], inplace = True)
    row = ['yeetus']

    rookie_data['TRB'] = rookie_data['TRB'] - rookie_data['ORB']

    rookie_data.rename(columns={'TRB': 'DRB'}, inplace = True)


    '''
    for col in rookie_data.columns: 
        if col != 'MP':
            rookie_data[col] = rookie_data[col].divide(rookie_data['MP'], fill_value = 1)

    rookie_data.drop(columns = ['MP'], inplace = True)



    print(rookie_data.head())
    '''

    for col in rookie_data.columns: 
        row.append(rookie_data[col].median())
    #player_stats = ['player', 'mp', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB','DRB','AST','STL','BLK','TOV','PF','PTS']
 
    return row
