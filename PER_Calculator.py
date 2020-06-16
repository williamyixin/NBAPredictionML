minutes_played
three_point
assist
factor
team_assist
team_field_goal
field_goal
free_throw
value_of_possession
turnover
defensive_rebound_percentage
field_goal_attempted
free_throw_attempted
total_rebound
offensive_redound
steal
blocks
personal_fouls
league_free_throws
league_personal_fouls
league_free_throws_attempted


PER = (1/minutes_played) * (three_point - 
    (personal_fouls * league_free_throws/league_personal_fouls) + 
    (free_throw/2) * (2 - team_assist/(3 * team_field_goal)) + 
    (field_goal * (2 - (factor * team_assist/team_field_goal))) +
    (2 * assist/3) + value_of_possession * 
    )