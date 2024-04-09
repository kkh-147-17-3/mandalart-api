from typing import Annotated

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Request, HTTPException, Depends, Query

from models.response import GenericResponse
from models.token import BaseTokenDto
from services.login import LoginService

router = InferringRouter()


@cbv(router)
class LoginView:
    login_service: LoginService = Depends(LoginService)

    @router.get("/login/kakao", tags=["login"], description="카카오 로그인 SDK를 통해 발급받은 access token을 이용하여 로그인합니다.")
    def kakao_login(self, access_token: Annotated[str, Query(alias="accessToken")]) -> GenericResponse[BaseTokenDto]:
        result = self.login_service.handle_login(access_token, "KAKAO")
        return GenericResponse(status=200, data=result, message="ok")
