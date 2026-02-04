# ⚽ Premier League Data Pipeline (Hybrid Architecture)

## Overview
A production-grade ETL pipeline designed for sports analytics. This solution implements a **Hybrid Data Architecture**, capturing raw JSON data in a NoSQL Data Lake (MongoDB) for data science usage, while simultaneously structuring finished match statistics into a normalized SQL Server database for BI reporting.

## 🏗 Architecture
**Source** (REST API) ➡️ **Python ETL** ➡️ **Data Lake** (MongoDB) ➡️ **Data Warehouse** (SQL Server)



## 🔧 Tech Stack & Best Practices
* **Python 3.10+**: Core ETL logic.
* **SQLAlchemy ORM**: Used for database interactions to avoid "SQL Injection" risks and raw string manipulation.
* **MongoDB**: Acts as the "Landing Zone" for raw API responses (handling schema drift).
* **MS SQL Server**: Normalized Star Schema for high-performance querying.
* **Security**: Environment variables (`.env`) used for API Key and DB Credential management.

## 🚀 Setup & Configuration

### 1. Prerequisites
* **Microsoft SQL Server** (Express or Developer edition)
* **MongoDB Community Server**
* **Python 3.x**

### 2. Get a Free API Key
This project uses the Football-Data.org API.
1.  Go to [https://www.football-data.org/client/register](https://www.football-data.org/client/register).
2.  Register to get your free API Token via email.

### 3. Install Dependencies
```bash
pip install -r requirements.txt

4. Configure Environment
Rename the file env.example to .env.

Open .env and paste your API Key:

Ini, TOML
FOOTBALL_API_KEY=your_actual_key_here
SQL_SERVER=.\SQLEXPRESS
DB_NAME=FootballAnalyticsDB
5. Run the Pipeline
Bash
python etl_pipeline.py
The script will automatically create the database tables if they do not exist.

📊 Analytics
Once the data is loaded, open SQL Server Management Studio (SSMS) and run the stored procedures in 02_analytics.sql to generate reports:

SQL
EXEC sp_GetLeagueTable;
