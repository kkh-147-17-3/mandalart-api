from typing import Annotated

from fastapi import Depends
from fastapi_oauth2.middleware import User
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.requests import Request

from services.token import TokenService
from oauth import on_auth

router = InferringRouter()


@cbv(router)
class TokenView:
    token_service: TokenService = Depends(TokenService)

    # @router.get("/token")
    def get_token(self, req: Request) -> dict:
        return self.token_service.get_token(req.user)
