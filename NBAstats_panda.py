import pandas as pd


data = pd.read_csv("Player_Data.csv", encoding='utf-8')
for col in data.columns:
    data[col] = data[col].str.decode('utf-8')
print(data)
print(data.dtypes)