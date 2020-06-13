from bs4 import BeautifulSoup
import requests
import csv



'''
Scrape Rushing/Passing Offense/Defense Stats by Conference
'''

conferences = ['905', '823', '821', '25354', '827', '24312', '99001', '875', '5486', '911', '818']
rush_off = 'Rush_Off.csv'
rush_off_headers =  ['Rank','Name','G','Att', 'Yards','Avg','TD',  'Att/G','Rush Offense Yards/G']

pass_off = 'Pass_Off.csv'
pass_off_headers = ['Rank','Name', 'G', 'Att', 'Comp', 'Pct', 'Yards', 'Yards/Att', 'TD',  'Int', 'Rating',  'Att/G', 'Pass Offense Yards/G']

rush_def = 'Rush_Def.csv'
rush_def_headers = ['Rank','Name','G', 'Att', 'Yards', 'Avg', 'TD', 'Att/G', 'Rush Defense Yards/G']

pass_def = 'Pass_Def.csv'
pass_def_headers = ['Rank', 'Name', 'G', 'Att', 'Comp', 'Pct.', 'Yards', 'Yards/Att', 'TD', 'Int', 'Rating', 'Att/G', 'Pass Defense Yards/G']

turnover_margin = 'Turnover_Margin.csv'
turnover_margin_headers = [ 'Rank', 'Name', 'G',   'Fum. Gain',   'Int. Gain',   'Total Gain',  'Fum. Lost', 'Int. Lost', 'Total Lost',  'Margin',  'Margin/G']

scoring_offense = 'Scoring_Off.csv'
scoring_offense_headers = ['Rank', 'Name', 'G', 'TD',  'FG',  '1XP', '2XP', 'Safety',  'Points',  'Points/G']

    # url = 'http://www.cfbstats.com/2014/leader/' + conference +'/team/offense/split01/category01/sort01.html'
        
    # r  = requests.get(url)

    # data = r.text

    # soup = BeautifulSoup(data, "html.parser")

    # table = soup.find('table')
    # print conference + " done"


with open(rush_off, 'wb+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = rush_off_headers, delimiter = ',')
    writer.writeheader()
    writer = csv.writer(csv_file)
    for conference in conferences:

        url = 'http://www.cfbstats.com/2014/leader/' + conference +'/team/offense/split01/category01/sort01.html'
            
        r  = requests.get(url)

        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find('table')
        # print conference + " rush offense done"
        for trs in table.find_all('tr'):
            tds = trs.find_all('td')
            row = [elem.text.strip().encode('utf-8') for elem in tds]
            #final_data.append(row)
            writer.writerow(row)
    print "rush offense done"
    #print final_data

#http://www.cfbstats.com/2014/leader/818/team/offense/split01/category02/sort01.html


with open(pass_off, 'wb+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = pass_off_headers, delimiter = ',')
    writer.writeheader()
    writer = csv.writer(csv_file)
    for conference in conferences:

        url = 'http://www.cfbstats.com/2014/leader/' + conference +'/team/offense/split01/category02/sort01.html'
            
        r  = requests.get(url)

        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find('table')
        # print conference + " pass offense done"
        for trs in table.find_all('tr'):
            tds = trs.find_all('td')
            row = [elem.text.strip().encode('utf-8') for elem in tds]
            #final_data.append(row)
            writer.writerow(row)
    print "pass offense done"

#http://www.cfbstats.com/2014/leader/905/team/defense/split01/category01/sort01.html

with open(rush_def, 'wb+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = rush_def_headers, delimiter = ',')
    writer.writeheader()
    writer = csv.writer(csv_file)
    for conference in conferences:

        url = 'http://www.cfbstats.com/2014/leader/' + conference +'/team/defense/split01/category01/sort01.html'
            
        r  = requests.get(url)

        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find('table')
        #print conference + " rush defense done"
        for trs in table.find_all('tr'):
            tds = trs.find_all('td')
            row = [elem.text.strip().encode('utf-8') for elem in tds]
            #final_data.append(row)
            writer.writerow(row)
    print "rush defense done"


#team/defense/split01/category02/sort01.html
with open(pass_def, 'wb+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = pass_def_headers, delimiter = ',')
    writer.writeheader()
    writer = csv.writer(csv_file)
    for conference in conferences:

        url = 'http://www.cfbstats.com/2014/leader/' + conference +'/team/defense/split01/category02/sort01.html'
            
        r  = requests.get(url)

        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find('table')
        #print conference + " pass defense done"
        for trs in table.find_all('tr'):
            tds = trs.find_all('td')
            row = [elem.text.strip().encode('utf-8') for elem in tds]
            #final_data.append(row)
            writer.writerow(row)
    print "pass defense done"

#http://www.cfbstats.com/2014/leader/905/team/offense/split01/category12/sort01.html


with open(turnover_margin, 'wb+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = turnover_margin_headers, delimiter = ',')
    writer.writeheader()
    writer = csv.writer(csv_file)
    for conference in conferences:

        url = 'http://www.cfbstats.com/2014/leader/' + conference +'/team/offense/split01/category12/sort01.html'
            
        r  = requests.get(url)

        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find('table')
        #print conference + " pass defense done"
        for trs in table.find_all('tr'):
            tds = trs.find_all('td')
            row = [elem.text.strip().encode('utf-8') for elem in tds]
            #final_data.append(row)
            writer.writerow(row)
    print "turnover margin done"

#http://www.cfbstats.com/2014/leader/823/team/offense/split01/category09/sort01.html

with open(scoring_offense, 'wb+') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = scoring_offense_headers, delimiter = ',')
    writer.writeheader()
    writer = csv.writer(csv_file)
    for conference in conferences:

        url = 'http://www.cfbstats.com/2014/leader/' + conference +'/team/offense/split01/category09/sort01.html'
            
        r  = requests.get(url)

        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find('table')
        #print conference + " pass defense done"
        for trs in table.find_all('tr'):
            tds = trs.find_all('td')
            row = [elem.text.strip().encode('utf-8') for elem in tds]
            #final_data.append(row)
            writer.writerow(row)
    print "scoring offense done"
