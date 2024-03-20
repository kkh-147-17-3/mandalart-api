import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_oauth2.middleware import Auth, User, OAuth2Middleware
from fastapi_oauth2.router import router as oauth2_router

from starlette.middleware.cors import CORSMiddleware

from database import Base, engine
from oauth import oauth2_config, on_auth
from views import user_router, token_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(oauth2_router)
app.include_router(user_router)
app.include_router(token_router)

app.add_middleware(OAuth2Middleware, config=oauth2_config, callback=on_auth)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )
