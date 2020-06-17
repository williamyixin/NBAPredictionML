import pandas as pd


data = pd.read_csv("Player_Data_pandas.csv", index_col=[1,2], encoding='utf-8')
data.dropna(axis=0, how='all',thresh=None,subset=None,inplace=True)
print(data)