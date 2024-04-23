import os
from datetime import timedelta, datetime, timezone
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from errors.exceptions import MissingEnvVarException, InvalidJwtException

load_dotenv('src/../.env')

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
security = HTTPBearer()

if not SECRET_KEY or not ALGORITHM:
    raise MissingEnvVarException("JWT_SECRET_KEY and JWT_ALGORITHM are required")


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    to_encode: Dict[str, Any] = {"user_id": user_id}
    now = datetime.now(tz=timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=1)
    to_encode.update({"exp": expire.replace(tzinfo=timezone.utc)})
    to_encode.update({"sub": "access_token"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    now = datetime.now(tz=timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=30)
    encoded_jwt = jwt.encode({
        "sub": "refresh_token",
        "exp": expire.replace(tzinfo=timezone.utc),
        "user_id": user_id
    }, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if payload['sub'] != "access_token":
            raise InvalidJwtException(code=40101, msg='Invalid token')
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise InvalidJwtException(code=40102, msg='Signature has expired')
    except jwt.JWTClaimsError as _:
        raise InvalidJwtException(code=40103, msg='Invalid token')


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
