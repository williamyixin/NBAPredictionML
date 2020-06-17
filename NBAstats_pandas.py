import pandas as pd

df = pd.read_csv('Player_Data.csv', encoding='cp1252')
df2 = pd.read_csv('Player_Data.csv')
print(df2.dtypes)