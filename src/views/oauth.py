from typing import Annotated

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, Query

from enums import SocialProvider
from models.token import BaseTokenDto
from services.login import LoginService
from services.token import auth_access_wrapper

router = InferringRouter()


@cbv(router)
class OAuthLoginView:
    login_service: LoginService = Depends(LoginService)

    @router.get("/oauth/kakao", tags=["oauth"])
    def kakao_login(self, code: Annotated[str, Query()]) -> BaseTokenDto:
        return self.login_service.handle_oauth_login(code,SocialProvider.KAKAO)

    @router.get("/login/apple")
    def apple_login(self, code: str):
        return self.login_service.handle_apple_login(code)

    @router.post("/sign-out/apple")
    def sign_out_apple(self, user_id: Annotated[int, Depends(auth_access_wrapper)]):
        return self.login_service.handle_apple_sign_out(user_id)
