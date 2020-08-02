import pandas as pd
import numpy as np
import os
import csv

direct = os.getcwd()
currentdata = pd.read_csv("updatedtrainingdata.csv", encoding='utf-8')
#currentdata = currentdata.drop(currentdata.index[0])
#currentdata = currentdata.drop(["GameID"], axis=1)
#currentdata.rename(columns={'Unnamed: 0': 'GameID'}, inplace=True)

path = direct + '/GameRows'
rows = os.listdir(path)
os.chdir("GameRows")
for row in rows:
    temp = pd.read_csv(row, encoding='utf-8')
    currentdata = currentdata.append(temp, ignore_index=True)
    os.remove(row)

currentdata.to_csv("../updatedtrainingdata.csv", encoding='utf-8', index=False)
#temp = pd.read_csv("../updatedtrainingdata.csv", encoding='utf-8')
#print(temp)