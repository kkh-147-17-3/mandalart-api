import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv


load_dotenv('./.env')
user = os.getenv("DB_USER")
passwd = os.getenv("DB_PASSWORD")
url = os.getenv("DB_URL")
db_database = os.getenv("DB_DATABASE")
engine = create_engine(f"postgresql://{user}:{passwd}@{url}:5432/{db_database}", echo=True)
session_local = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
