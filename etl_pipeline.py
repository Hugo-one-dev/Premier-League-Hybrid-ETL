import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import exists
from pymongo import MongoClient


load_dotenv()

API_KEY = os.getenv('FOOTBALL_API_KEY')
SERVER = os.getenv('SQL_SERVER')
DB_NAME = os.getenv('DB_NAME')

if not API_KEY:
    print(" ERROR: API Key not found. Check your .env file.")
    exit()

connection_string = f'mssql+pyodbc://{SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes'
sql_engine = create_engine(connection_string)
Base = declarative_base()

mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['FootballRawLake']
mongo_collection = mongo_db['matches_json']

print("Connected to SQL Server & MongoDB.")



class Team(Base):
    __tablename__ = 'DimTeams'
    TeamID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    ShortName = Column(String(50))
    TLA = Column(String(3))
    CrestUrl = Column(String(255))

class Match(Base):
    __tablename__ = 'FactMatches'
    MatchID = Column(Integer, primary_key=True)
    Date = Column(DateTime)
    HomeTeamID = Column(Integer, ForeignKey('DimTeams.TeamID'))
    AwayTeamID = Column(Integer, ForeignKey('DimTeams.TeamID'))
    HomeScore = Column(Integer)
    AwayScore = Column(Integer)
    Winner = Column(String(20))
    Status = Column(String(20))

Base.metadata.create_all(sql_engine)
Session = sessionmaker(bind=sql_engine)
session = Session()


print(" Fetching data from API...")
url = 'https://api.football-data.org/v4/competitions/PL/matches'
headers = {'X-Auth-Token': API_KEY}

response = requests.get(url, headers=headers)
data = response.json()

if 'matches' not in data:
    print(" API Error or No Data Found")
    exit()

matches = data['matches']
print(f" Downloaded {len(matches)} matches.")

print(" Saving Raw JSON to MongoDB...")
for match in matches:
    mongo_collection.update_one(
        {'id': match['id']}, 
        {'$set': match}, 
        upsert=True
    )

print("  Transforming & Loading to SQL Server...")

for match in matches:
    if match['status'] != 'FINISHED':
        continue 
    
    def get_or_create_team(team_data):
        team = session.query(Team).filter_by(TeamID=team_data['id']).first()
        if not team:
            team = Team(
                TeamID=team_data['id'],
                Name=team_data['name'],
                ShortName=team_data['shortName'],
                TLA=team_data['tla'],
                CrestUrl=team_data['crest']
            )
            session.add(team)
            session.commit()
        return team

  
    get_or_create_team(match['homeTeam'])
    get_or_create_team(match['awayTeam'])

    match_id = match['id']
    existing_match = session.query(Match).filter_by(MatchID=match_id).first()
    
 
    h_score = match['score']['fullTime']['home']
    a_score = match['score']['fullTime']['away']
    if h_score > a_score: winner = 'HOME_TEAM'
    elif a_score > h_score: winner = 'AWAY_TEAM'
    else: winner = 'DRAW'

    if existing_match:
        existing_match.Status = match['status']
        existing_match.HomeScore = h_score
        existing_match.AwayScore = a_score
        existing_match.Winner = winner
    else:
        new_match = Match(
            MatchID=match_id,
            Date=match['utcDate'],
            HomeTeamID=match['homeTeam']['id'],
            AwayTeamID=match['awayTeam']['id'],
            HomeScore=h_score,
            AwayScore=a_score,
            Winner=winner,
            Status=match['status']
        )
        session.add(new_match)

session.commit()
print(" ETL Pipeline Finished Successfully.")