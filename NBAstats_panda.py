import pandas as pd


data = pd.read_csv("Player_Data.csv", encoding='utf-8')
data = data.astype("string")
data.apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
#for col in data.columns:
 #   data[col] = data[col].str.slice(2, -1)

#data['Minutes Played'] = pd.to_numeric(data['Minutes Played'])
#data['PER'] = pd.to_numeric(data['PER'])
print(data)
print(data.dtypes)