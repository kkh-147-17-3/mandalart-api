from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(f"postgresql://{user}:{passwd}@{url}:5432/{db}")

session_local = sessionmaker(autocommit=False, bind=engine)


def get_db():
    db = session_local()
    try:
        print('db connected')
        yield db
    finally:
        print("db close...")
        db.close()
