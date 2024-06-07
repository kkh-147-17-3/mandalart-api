import atexit
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
import traceback

from fastapi_oauth2.config import OAuth2Config
from fastapi_oauth2.middleware import OAuth2Middleware
from fastapi_oauth2.router import router as oauth2_router

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import ValidationException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import ENCODERS_BY_TYPE
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from database import Base, engine
from errors.exceptions import EntityNotFoundException, UnauthorizedException, InvalidJwtException
from models.response import ErrorResponse
from oauth import on_auth, oauth2_config
from scheduler import scheduler
from views import routers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_: FastAPI):
    ENCODERS_BY_TYPE[datetime] = lambda date_obj: date_obj.strftime("%Y-%m-%d %H:%M:%S")
    queue_handler = logging.getHandlerByName('queue_handler')
    if queue_handler is not None:
        queue_handler.listener.start()  # type: ignore
        atexit.register(queue_handler.listener.stop)  # type: ignore
    scheduler.start()
    yield


app = FastAPI(
    title="eggtart API",
    description="eggtart API에 대한 docs입니다.",
    lifespan=lifespan,
    responses={
        422: {"status": 422, "description": "Validation Error", "model": ErrorResponse}
    }
)

for router in routers:
    app.include_router(router)

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


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(_: Request, exc: UnauthorizedException):
    res_code = status.HTTP_401_UNAUTHORIZED
    return JSONResponse(
        status_code=res_code,
        content={"status": res_code, "message": exc.msg}
    )


@app.exception_handler(EntityNotFoundException)
async def entity_not_found_exception_handler(_: Request, exc: EntityNotFoundException):
    res_code = status.HTTP_404_NOT_FOUND
    return JSONResponse(
        status_code=res_code,
        content={"status": res_code, "message": str(exc)}
    )


@app.exception_handler(InvalidJwtException)
async def invalid_jwt_exception_handler(_: Request, exc: InvalidJwtException):
    res_code = status.HTTP_401_UNAUTHORIZED
    return JSONResponse(
        status_code=res_code,
        content={"status": exc.code, "message": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(_: Request, exc: Exception):
    res_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(
        status_code=res_code,
        content={"status": res_code, "data": traceback.format_exc(5), "message": str(exc)}
    )


logger = logging.getLogger("main")

# @app.middleware('http')
# async def log_api_request_and_response(request: Request, call_next: Callable[[Any], Awaitable[StreamingResponse]]):
#     response = await call_next(request)
#     response_body = b""
#     async for chunk in response.body_iterator:
#         response_body += chunk
#     logger.info({
#         "method": request.method,
#         "url": request.url,
#         "headers": request.headers,
#         "query_params": request.query_params,
#         "path_params": request.path_params,
#         "request_body": await request.body(),
#         "response_status": response.status_code,
#         "response_headers": response.headers,
#         "response_body": response_body
#     })
#     return Response(content=response_body, status_code=response.status_code,
#                     headers=dict(response.headers), media_type=response.media_type)
