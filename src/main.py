import os
from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.encoders import ENCODERS_BY_TYPE
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from database import Base, engine
from views import user_router, token_router, sheet_router, cell_router, healthcheck_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ENCODERS_BY_TYPE[datetime] = lambda date_obj: date_obj.strftime("%Y-%m-%d %H:%M:%S")
    yield


app = FastAPI(
    title="eggtart API",
    description="eggtart API에 대한 docs입니다.",
    lifespan=lifespan
)
# app.include_router(oauth2_router)
app.include_router(user_router)
app.include_router(token_router)
app.include_router(sheet_router)
app.include_router(cell_router)
app.include_router(healthcheck_router)

# app.add_middleware(OAuth2Middleware, config=oauth2_config, callback=on_auth)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )
