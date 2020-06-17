
# function that calculates a given player's adjusted PER
def aPER_Calculator(MP, threeP, AST, lg_AST, lg_FG, lg_FT, team_AST, team_FG, FG, FTA, FT, lg_PTS, lg_FGA, lg_ORB, lg_TOV, lg_FTA, TOV, lg_TRB, FGA, TRB, ORB, STL, BLK, PF, lg_PF, lg_Pace, team_Pace):
    # calculate factor
    Factor = Factor_Calculator(lg_AST, lg_FG, lg_FT)
    
    # calculate value of possession
    VOP = VOP_Calculator(lg_PTS, lg_FGA, lg_ORB, lg_TOV, lg_FTA)
    
    # calculate defensive rebound percentage 
    DRB = DRB_Calculator(lg_TRB, lg_ORB)
    
    # calculate pace adjustment
    pace = Pace_Adjustment(lg_Pace, team_Pace)
    
    # main formula for unadjusted PER
    uPER = ((1 / MP) * 
        [threeP 
        + (2 / 3) * AST 
        + (2 - Factor * (team_AST / team_FG)) * FG 
        + (FT * 0.5 * (1 + (1 - (team_AST / team_FG)) 
        + (2 / 3) * (team_AST / team_FG))) 
        - VOP *TOV 
        - VOP * DRB * (FGA - FG) 
        - VOP * 0.44 * (0.44 + (0.56 * DRB)) * (FTA - FT) 
        + VOP * (1 - DRB) * (TRB - ORB) 
        + VOP * DRB * ORB 
        + VOP * STL 
        + VOP * DRB * BLK 
        - PF * ((lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP)])

    # return adjusted PER
    return (pace* uPER)

# function that calculates the factor part of the PER equation
def Factor_Calculator(lg_AST, lg_FG, lg_FT):
    return ((2 / 3) - (0.5 * (lg_AST / lg_FG)) / (2 * (lg_FG / lg_FT)))

# function that calculates the value of possession part of the PER equation
def VOP_Calculator(lg_PTS, lg_FGA, lg_ORB, lg_TOV, lg_FTA):
    return (lg_PTS / (lg_FGA - lg_ORB + lg_TOV + 0.44 * lg_FTA))

# function that calculates the defensive rebound percentage part of the PER equation
def DRB_Calculator(lg_TRB, lg_ORB):
    return ((lg_TRB - lg_ORB) / lg_TRB)

# function that calculates the pace adjustment part of the PER equation
def Pace_Adjustment(lg_Pace, team_Pace):
    return (lg_Pace / team_Pace)

# takes a list of adjusted PERs and standardizes them so that the average is 15
def PER_Calculator(aPERs):
    lg_aPER = aPERs.mean()
    for elem in aPERs:
        elem = elem * (15 / lg_aPER)
    return aPERs