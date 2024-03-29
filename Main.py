import NBAstats_scrape

'''
Generates the training data.
'''

years = [2021, 2022]

minutes_threshold = 100

for year in years: 
    NBAstats_scrape.generate_previous_season(year)
    game_links = NBAstats_scrape.get_game_links(year)
    team_abbreviations = NBAstats_scrape.get_team_names(year)
    
    