import pandas as pd
"""
from datetime import datetime
from datetime import date
from datetime import timedelta

curr = datetime.today().strftime('%Y-%m-%d').split('-')
curryear = int(curr[0])
currmonth = int(curr[1])
currday = int(curr[2])

startmonth = -1
startday = -1
startyear = -1
"""

#Download latest data
statpath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/statline.csv'
stats = pd.read_csv(statpath).drop(columns = 'Unnamed: 0')
dfspath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/dfs.csv'
dfs = pd.read_csv(dfspath).drop(columns = 'Unnamed: 0')
draftkingspath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/draftkings.csv'
dfk = pd.read_csv(draftkingspath).drop(columns = 'Unnamed: 0')
fanduelpath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/fanduel.csv'
fanduel = pd.read_csv(fanduelpath).drop(columns = 'Unnamed: 0')

def getPlayerStats(name):
    """Get projected stats of specific player"""
    return stats[stats['Name'] == name]

def getTeamStats(team):
    """Get projected stats of all players from certain team"""
    return stats[stats['Team'] == team.upper()]

def scoresOver(fantasy, score):
    """Get players with scores over score based on DraftKings or FanDuel"""
    if fantasy.lower() == 'fanduel':
        return dfs[dfs['Projected Fanduel Points'] > score]
    elif fantasy.lower() == 'draftkings':
        return dfs[dfs['Projected Draftkings Points'] > score]
    else:
        assert False

def fanduelOptimal():
    """Get the fanduel optimal lineup"""
    return fanduel

def draftkingsOptimal():
    """Get the draftkings optimal lineup"""
    return dfk

def statsOver(stat, value):
    """Get players with stat values over value for a certain statistic
    (points, rebounds, assists, etc...)"""
    assert stat in ['Minutes', '2PT FG', '3PT FG', 'FTM', 'Rebounds', 'Assists', 'Blocks', 'Steals', 'Turnovers']
    return stats[stats[stat] > value]

def getInjured():
    """Get names and injury types for all injured players"""
    return stats[stats['Injury Indicator'] != ' ']['Name']

def getAllStats():
    """Get daily projections for all players"""
    return stats

def getAllProjections():
    """Get all projections from fanduel and draftkings"""
    return dfs

"""
def setDate(m, d, y):
    currmonth = m
    currday = d
    curryear = y
    statpath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/statline.csv'
    stats = pd.read_csv(statpath).drop(columns = 'Unnamed: 0')
    dfspath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/dfs.csv'
    dfs = pd.read_csv(dfspath).drop(columns = 'Unnamed: 0')
    draftkingspath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/draftkings.csv'
    dfk = pd.read_csv(draftkingspath).drop(columns = 'Unnamed: 0')
    fanduelpath = 'https://raw.githubusercontent.com/BerkeleySportsAnalytics/sagb-site/master/dfs/inputs/fanduel.csv'
    fanduel = pd.read_csv(fanduelpath).drop(columns = 'Unnamed: 0')

def getRangeStats(m1, d1, y1, m2, d2, y2):
    start_date = date(y1, m1, d1)
    end_date = date(y2, m2, d2)
    assert end_date > start_date
    out = stats.copy()
    out['Date'] = [start_date for i in range(len(out))]
    while start_date != end_date:
        setDate(start_date.month, start_date.day, start_date.year)
        start_date += timedelta(1)
        temp = stats.copy()
        temp['Date'] = [start_date for i in range(len(temp))]
        out = pd.concat([out, temp])
    return out

def getRangeProjections(m1, d1, y1, m2, d2, y2):
    start_date = date(y1, m1, d1)
    end_date = date(y2, m2, d2)
    assert end_date > start_date
    out = dfs.copy()
    out['Date'] = [start_date for i in range(len(out))]
    while start_date != end_date:
        setDate(start_date.month, start_date.day, start_date.year)
        start_date += timedelta(1)
        temp = dfs.copy()
        temp['Date'] = [start_date for i in range(len(temp))]
        out = pd.concat([out, temp])
    return out

def getAllStats():
    return getRangeStats(startmonth, startday, startyear)

def getAllProjections():
    return getRangeProjections(startmonth, startday, startyear)
"""

def getStatsPerMinute():
    """Get per minute stats of the model's prediction"""
    perMinute = stats.copy()
    perMinute['2PT FG'] /= perMinute['Minutes']
    perMinute['3PT FG'] /= perMinute['Minutes']
    perMinute['FTM'] /= perMinute['Minutes']
    perMinute['Rebounds'] /= perMinute['Minutes']
    perMinute['Assists'] /= perMinute['Minutes']
    perMinute['Blocks'] /= perMinute['Minutes']
    perMinute['Steals'] /= perMinute['Minutes']
    perMinute['Turnovers'] /= perMinute['Minutes']
    return perMinute

"""
def buildMultipleLineups(n):
    pass
"""

if __name__ == "__main__": #Test API Functions
    #print(getPlayerStats('Jimmy Butler'))
    #print(getTeamStats('BKN'))
    #print(statsOver('Rebounds', 10))
    #print(getAllProjections())
    #print(scoresOver('fanduel', 40))
    #print(scoresOver('draftkings', 40))
    #getPlayerStats('James Harden')
    #setDate(8, 4, 2020)
    #getPlayerStats('James Harden')
    #print(getStatsPerMinute().head()[['2PT FG', '3PT FG', 'FTM', 'Rebounds', 'Assists',
    #'Blocks', 'Steals', 'Turnovers']])
