from typing import Annotated

from fastapi import Depends
from fastapi_oauth2.middleware import User
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.requests import Request

from models.response import GenericResponse
from models.token import BaseTokenDto
from services.token import auth_refresh_wrapper
from services.login import get_token

router = InferringRouter()


@cbv(router)
class TokenView:

    @router.get("/token", tags=["login"],
                summary="refresh token을 사용하여 새로운 access token과 refresh token을 발급받습니다.",
                description="Authorization 헤더에 access token 대신 refresh token을 사용하여 새로운 token을 발급받습니다."
                )
    def get_token(self, user_id: int = Depends(auth_refresh_wrapper)) -> GenericResponse[BaseTokenDto]:
        token_dto = get_token(user_id)
        return GenericResponse(status=200, data=token_dto, message="OK")
