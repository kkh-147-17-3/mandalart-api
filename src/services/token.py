from datetime import timedelta, datetime, timezone
from typing import Dict, Any

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
security = HTTPBearer()


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    to_encode: Dict[str, Any] = {"user_id": user_id}
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire})
    to_encode.update({"sub": "access_token"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=30)
    encoded_jwt = jwt.encode({
        "sub": "refresh_token",
        "exp": expire,
        "user_id": user_id
    }, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if payload['sub'] != "access_token":
            raise HTTPException(status_code=401, detail='Invalid token')
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except jwt.JWTClaimsError as _:
        raise HTTPException(status_code=401, detail='Invalid token')


def decode_refresh_token(token) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if payload['sub'] != "refresh_token":
            raise HTTPException(status_code=401, detail='Invalid token')
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has been expired')
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail='Invalid token')


def auth_access_wrapper(auth: HTTPAuthorizationCredentials = Depends(security)):
    return decode_access_token(auth.credentials)


def auth_refresh_wrapper(auth: HTTPAuthorizationCredentials = Depends(security)):
    return decode_refresh_token(auth.credentials)
