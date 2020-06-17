minutes_played = 1564
three_point = 1
assist = 141
factor = (2/3) - ((0.5 * league_assists/league_field_goals)
    / (2 * league_field_goals/league_free_throws))
team_assist = 1400
team_field_goal = 5447
field_goal = 262
free_throw = 108
value_of_possession = (league_points / 
    (league_field_goals_attempted - league_offensive_rebound +
    league_turnover + 0.44 * league_free_throws_attempted))
turnover = 86
defensive_rebound_percentage = (league_total_rebound - league_offensive_rebound)/league_total_rebound
field_goal_attempted = 443
free_throw_attempted = 183
total_rebound = 543
offensive_rebound = 196
steal = 50
blocks = 65
personal_fouls = 111
league_free_throws
league_personal_fouls
league_free_throws_attempted
league_assists
league_field_goals
league_points
league_field_goals_attempted
league_offensive_rebound
league_turnover
league_total_rebound


PER = (1/minutes_played) * (three_point - 
    (personal_fouls * league_free_throws/league_personal_fouls) + 
    (free_throw/2) * (2 - team_assist/(3 * team_field_goal)) + 
    (field_goal * (2 - (factor * team_assist/team_field_goal))) +
    (2 * assist/3) + value_of_possession * (defensive_rebound_percentage * 
    (2 * offensive_rebound + blocks - 0.2464 * 
    (free_throw_attempted - free_throw) - (field_goal_attempted - field_goal) - total_rebound)
    + (0.44 * league_free_throws_attempted * personal_fouls/league_personal_fouls) 
    - (turnover + offensive_rebound) + steal + total_rebound - 0.1936
    (free_throw_attempted - free_throw)))






