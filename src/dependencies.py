from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database import session_local
from jwt import decode_jwt_token

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
