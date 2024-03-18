import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_oauth2.claims import Claims
from fastapi_oauth2.client import OAuth2Client
from fastapi_oauth2.middleware import OAuth2Middleware, OAuth2Config, Auth, User
from fastapi_oauth2.router import router as oauth2_router
from social_core.backends import kakao, google

from views import user_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.include_router(oauth2_router)
app.include_router(user_router)

oauth2_config = OAuth2Config(
    allow_http=True,
    jwt_secret="secret",
    jwt_expires=900,
    jwt_algorithm="HS256",
    clients=[
        OAuth2Client(
            backend=kakao.KakaoOAuth2,
            client_id=kakao_client_id,
            client_secret=kakao_client_secret,
            scope=["profile_nickname", "profile_image", "gender"],
            claims=Claims(
                identity=lambda user: f"{user.provider}:{user.sub}",
            ),
        ),
        OAuth2Client(
            backend=google.GoogleOAuth2,
            client_id=google_client_id,
            client_secret=google_client_secret,
            scope=["email", "profile"],
            claims=Claims(
                identity=lambda user: f"{user.provider}:{user.sub}",
            ),
        ),
    ]
)


async def on_auth(auth: Auth, user: User):
    print(auth, user)


app.add_middleware(OAuth2Middleware, config=oauth2_config, callback=on_auth)
