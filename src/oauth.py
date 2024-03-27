import os

from dotenv import load_dotenv
from fastapi_oauth2.claims import Claims
from fastapi_oauth2.client import OAuth2Client
from fastapi_oauth2.config import OAuth2Config
from fastapi_oauth2.middleware import Auth, User
from social_core.backends import kakao
load_dotenv('./.env')
oauth2_config = OAuth2Config(
    allow_http=True,
    jwt_secret="secret",
    jwt_expires=900,
    jwt_algorithm="HS256",
    clients=[
        OAuth2Client(
            backend=kakao.KakaoOAuth2,
            client_id=os.getenv("KAKAO_ID"),
            client_secret=os.getenv("KAKAO_SECRET"),
            redirect_uri="http://localhost:8000/token",
            scope=["profile_nickname", "profile_image", "gender"],
            claims=Claims(
                identity=lambda user: f"{user.provider}:{user.sub}",
            ),
        ),
    ]
)


async def on_auth(auth: Auth, user: User) -> User:
    return user
