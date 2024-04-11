from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

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
    def get_token(self, user_id: int = Depends(auth_refresh_wrapper)) -> BaseTokenDto:
        return get_token(user_id)
