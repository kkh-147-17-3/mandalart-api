from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database import session_local
from src.jwt import decode_jwt_token

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

oauth2_scheme = HTTPBearer()
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def get_user_id(authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]) -> int:
    token = authorization.credentials
    return decode_jwt_token(token)['user_id']



