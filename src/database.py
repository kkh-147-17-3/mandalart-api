import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '../.env'))

user = os.getenv("DB_USER")
passwd = os.getenv("DB_PASSWORD")
url = os.getenv("DB_URL")
db_database = os.getenv("DB_DATABASE")
engine = create_engine(f"postgresql://{user}:{passwd}@{url}:5432/{db_database}")
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
