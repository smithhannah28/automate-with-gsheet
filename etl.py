import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine

# --- Config ---
SHEET_ID = "1npJZrNb30OgCpLTNEVwSQw1T6QqdQvdPbEDp8s3iNcg"   # from the URL: /spreadsheets/d/<THIS>/edit
WORKSHEET = "Sheet1"               # name of the tab you want to read

# --- Authenticate using your service account JSON ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

PATH_TO_JSON="extra/dafs-m07d07-ex01-4e4c15593bd1.json" # REPLACE WITH YOUR SERVICE ACCOUNT KEY FILE

creds = Credentials.from_service_account_file(PATH_TO_JSON, scopes=SCOPES)
gc = gspread.authorize(creds)

# --- Open the sheet ---
sh = gc.open_by_key(SHEET_ID)
ws = sh.worksheet(WORKSHEET)

# --- Read data into pandas ---
records = ws.get_all_records()     # gets all rows as list of dicts (first row = headers)
df = pd.DataFrame(records)

# Replace these credentials with your own PostgreSQL / RDS instance
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "host.docker.internal" # ⚠️ THIS IS IMPORTANT. Use that if you are running your notebook inside another container, otherwise you can use localhost
DB_PORT = "5432"
DB_NAME = "finance"

# Create a connection engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Load the dataframe into a new table called "pnl"
df.to_sql("pnl", engine, if_exists="replace", index=False)
