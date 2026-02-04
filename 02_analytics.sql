

USE FootballAnalyticsDB;
GO


CREATE OR ALTER PROCEDURE sp_GetLeagueTable
AS
BEGIN
    SELECT 
        T.Name AS Team,
        COUNT(M.MatchID) AS MatchesPlayed,
        SUM(CASE 
            WHEN M.HomeTeamID = T.TeamID AND M.Winner = 'HOME_TEAM' THEN 1
            WHEN M.AwayTeamID = T.TeamID AND M.Winner = 'AWAY_TEAM' THEN 1
            ELSE 0 END) AS Wins,
        SUM(CASE WHEN M.Winner = 'DRAW' THEN 1 ELSE 0 END) AS Draws,
        SUM(CASE 
            WHEN M.HomeTeamID = T.TeamID AND M.Winner = 'AWAY_TEAM' THEN 1
            WHEN M.AwayTeamID = T.TeamID AND M.Winner = 'HOME_TEAM' THEN 1
            ELSE 0 END) AS Losses,
        (SUM(CASE 
            WHEN M.HomeTeamID = T.TeamID AND M.Winner = 'HOME_TEAM' THEN 3
            WHEN M.AwayTeamID = T.TeamID AND M.Winner = 'AWAY_TEAM' THEN 3
            ELSE 0 END) +
         SUM(CASE WHEN M.Winner = 'DRAW' THEN 1 ELSE 0 END)) AS Points
    FROM dbo.DimTeams T
    JOIN dbo.FactMatches M ON T.TeamID = M.HomeTeamID OR T.TeamID = M.AwayTeamID
    WHERE M.Status = 'FINISHED'
    GROUP BY T.Name
    ORDER BY Points DESC;
END;
GO

CREATE OR ALTER PROCEDURE sp_GetTeamStats
    @TeamName NVARCHAR(100)
AS
BEGIN
    SELECT 
        T.Name,
        COUNT(M.MatchID) as GamesPlayed,
        SUM(CASE WHEN (T.TeamID = M.HomeTeamID AND M.HomeScore > M.AwayScore) OR 
                      (T.TeamID = M.AwayTeamID AND M.AwayScore > M.HomeScore) THEN 1 ELSE 0 END) as TotalWins
    FROM dbo.DimTeams T
    JOIN dbo.FactMatches M ON T.TeamID = M.HomeTeamID OR T.TeamID = M.AwayTeamID
    WHERE T.Name LIKE '%' + @TeamName + '%' 
      AND M.Status = 'FINISHED'
    GROUP BY T.Name;
END;
GO