

CREATE DATABASE FootballAnalyticsDB;
GO

USE FootballAnalyticsDB;
GO

CREATE TABLE dbo.DimTeams (
    TeamID INT PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    ShortName NVARCHAR(50),
    TLA CHAR(3),
    CrestUrl NVARCHAR(255)
);
GO


CREATE TABLE dbo.FactMatches (
    MatchID INT PRIMARY KEY,
    Date DATETIME NOT NULL,
    HomeTeamID INT NOT NULL,
    AwayTeamID INT NOT NULL,
    HomeScore INT,
    AwayScore INT,
    Winner NVARCHAR(20),
    Status NVARCHAR(20),

    CONSTRAINT FK_HomeTeam FOREIGN KEY (HomeTeamID) REFERENCES dbo.DimTeams(TeamID),
    CONSTRAINT FK_AwayTeam FOREIGN KEY (AwayTeamID) REFERENCES dbo.DimTeams(TeamID)
);
GO