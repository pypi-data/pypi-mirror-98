This is a module that allows you to query NBA Daily Fantasy Projections from Berkeley's Sports Analytics Group (SAGB).

getPlayerStats(name) - returns statline projections for specific player name if they are playing today


getTeamStats(team) - returns statline projections for specific team if they are playing today, requires 3 letter team abbreviation


scoresOver(fantasy, score) - Get players with scores over a specified score based on Draftkings or Fanduel, pass in either fanduel or draftkings to the fantasy argument


fanduelOptimal() - returns FanDuel optimal lineup


draftkingsOptimal() - returns DraftKings optimal lineup


statsOver(stat, value) - returns statline projections for players with a stat (Minutes, 2 PT FG, 3 PT FG, FTM, Rebounds, Assists, Blocks, Steals, Turnovers) over a certain value


getInjured() - names and injury types for all injured players


getAllStats() - returns all statline projections for the day


getAllProjections() - returns all fanduel and draftkings score projections for the day

getStatsPerMinute() - returns projected statline with per minute numbers