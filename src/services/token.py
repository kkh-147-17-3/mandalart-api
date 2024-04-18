import os
from datetime import timedelta, datetime, timezone
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from errors.exceptions import MissingEnvVarException

load_dotenv('src/../.env')

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
security = HTTPBearer()

if not SECRET_KEY or not ALGORITHM:
    raise MissingEnvVarException("JWT_SECRET_KEY and JWT_ALGORITHM are required")


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

APPLE_CLIENT_SECRET="-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgxo8hO7L5VNWIdUL/WSKk3xBjHCqd5f0NscPw7ZYxzkagCgYIKoZIzj0DAQehRANCAARmoPoS7s0xDt7rDjjllmeIc4poIBujC+DFp5tIlw3ep3MdOLM3p3ljYeUHo3s4tpWAO1ke69NKo7KvM3T6P2iC\n-----END PRIVATE KEY-----"


def create_apple_client_secret():
    alg = "ES256"
    issued_at = datetime.now()
    expire = datetime.now() + timedelta(days=30)

    return jwt.encode({
        "sub": "com.baker.eggtart.in",
        "exp": int(expire.timestamp()),
        "iat": int(issued_at.timestamp()),
        "iss": "SUMATJC294",
        "aud": "https://appleid.apple.com"
    }, APPLE_CLIENT_SECRET, algorithm=alg, headers={
        "alg": alg,
        "kid": "6QR4HWWN33"
    })