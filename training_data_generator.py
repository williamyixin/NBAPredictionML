import NBAstats_scrape

'''
Generates the training data.
'''

years = [2018]

minutes_threshold = 100

for year in years: 
    NBAstats_scrape.generate_previous_season(year)
    game_links = NBAstats_scrape.get_game_links(year)




