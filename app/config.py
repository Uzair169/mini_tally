import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "postgresql+psycopg2://postgres:postgres@localhost:5432/tallydb")