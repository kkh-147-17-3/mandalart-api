from typing import Annotated

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, Query

from models.token import BaseTokenDto
from services.login import LoginService
from services.token import auth_access_wrapper

router = InferringRouter()


@cbv(router)
class LoginView:
    login_service: LoginService = Depends(LoginService)

    @router.get("/login/kakao",
                tags=["login"],
                description="카카오 로그인 SDK를 통해 발급받은 access token을 이용하여 로그인합니다.<br/>"
                            "서버에 계정이 없는 경우 자동으로 추가됩니다. 로그인 성공 시 access token과 refresh token을 반환받습니다.<br/>"
                            " (유효기간: access token - 1일, refresh token - 30일)<br/>"
                            "*카카오 닉네임이 자동으로 서비스 닉네임으로 저장됩니다."
                )
    def kakao_login(self, access_token: Annotated[str, Query(alias="accessToken")],
                    short: Annotated[bool, Query()] = False) -> BaseTokenDto:
        return self.login_service.handle_login(access_token, "KAKAO", short)

    @router.get("/login/apple")
    def apple_login(self, code: str):
        return self.login_service.handle_apple_login(code)

    @router.post("/sign-out/apple")
    def sign_out_apple(self, user_id: Annotated[int, Depends(auth_access_wrapper)]):
        return self.login_service.handle_apple_sign_out(user_id)
