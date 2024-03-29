import os
from contextlib import asynccontextmanager
from datetime import datetime
import traceback
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import ValidationException, RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import ENCODERS_BY_TYPE
from starlette import status
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from database import Base, engine
from errors.error import EntityNotFoundException
from models.response import GenericResponse, ErrorResponse
from views import user_router, token_router, sheet_router, cell_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_: FastAPI):
    ENCODERS_BY_TYPE[datetime] = lambda date_obj: date_obj.strftime("%Y-%m-%d %H:%M:%S")
    yield


app = FastAPI(
    title="eggtart API",
    description="eggtart API에 대한 docs입니다.",
    lifespan=lifespan,
    responses={
        422: {"status": 422, "description": "Validation Error", "model": ErrorResponse}
    }
)
# app.include_router(oauth2_router)
app.include_router(user_router)
app.include_router(token_router)
app.include_router(sheet_router)
app.include_router(cell_router)

# app.add_middleware(OAuth2Middleware, config=oauth2_config, callback=on_auth)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: ValidationException):
    res_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(
        status_code=res_code,
        content={"status": res_code, "data": exc.errors(), "message": "Request validation error"}
    )


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(_: Request, exc: ValidationException):
    res_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(
        status_code=res_code,
        content={"status": res_code, "data": exc.errors(), "message": "Response validation error"}
    )


@app.exception_handler(EntityNotFoundException)
async def validation_exception_handler(_: Request, exc: EntityNotFoundException):
    res_code = status.HTTP_404_NOT_FOUND
    return JSONResponse(
        status_code=res_code,
        content={"status": res_code, "data": None, "message": str(exc)}
    )


@app.exception_handler(Exception)
async def validation_exception_handler(_: Request, exc: Exception):
    res_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(
        status_code=res_code,
        content={"status": res_code, "data": traceback.format_exc(5), "message": str(exc)}
    )
