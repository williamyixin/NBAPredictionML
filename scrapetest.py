import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
'''
url = 'https://www.basketball-reference.com/boxscores/201710170CLE.html'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "html.parser")
table = soup.find('table')
all_rows = []
for trs in table.find_all('tr'):
    row = []
    th = trs.find('th')
    row.append(th.text.strip())
    tds = trs.find_all('td')
    for cell in tds:
        row.append(cell.text.strip())
    if row:
        all_rows.append(row)

df = pd.DataFrame(data=all_rows)
df.dropna(inplace=True)
print(df)
'''
url = 'https://www.basketball-reference.com/boxscores/201710170CLE.html'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "html.parser")
table = soup.find_all('table')
print(table)

