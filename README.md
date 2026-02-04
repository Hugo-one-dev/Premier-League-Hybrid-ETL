#  Premier League Data Pipeline (Hybrid Architecture)

## Overview
A production-grade ETL pipeline designed for sports analytics. This solution implements a **Hybrid Data Architecture**, capturing raw JSON data in a NoSQL Data Lake (MongoDB) for data science usage, while simultaneously structuring finished match statistics into a normalized SQL Server database for BI reporting.

## 🏗 Architecture
**Source** (REST API) -> **Python ETL** -> **Data Lake** (MongoDB) -> **Data Warehouse** (SQL Server)

##  Tech Stack & Best Practices
* **Python 3.10+**: Core ETL logic.
* **SQLAlchemy ORM**: Used for database interactions to avoid "SQL Injection" risks and raw string manipulation.
* **MongoDB**: Acts as the "Landing Zone" for raw API responses (handling schema drift).
* **MS SQL Server**: Normalized Star Schema for high-performance querying.
* **Security**: Environment variables (`.env`) used for API Key and DB Credential management.

##  How to Run
1.  **Prerequisites:**
    * Install SQL Server & MongoDB Community Server.
    * Create a `.env` file (see `env.example`).
2.  **Install Dependencies:**
    ```bash
    pip install sqlalchemy pymongo python-dotenv pandas pyodbc
    ```
3.  **Execute Pipeline:**
    ```bash
    python etl_pipeline.py
    ```
    *This script creates the Schema automatically using SQLAlchemy models.*

## Analytics
Once the data is loaded, you can run the included Stored Procedures in `02_analytics.sql` to generate the League Table.
