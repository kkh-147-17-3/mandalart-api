from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException

from enums import SocialProvider
from models.token import BaseTokenDto
from models.user import BaseUserDto
import httpx
from models import kakaologinapi
from repositories import UserRepository
from schemas import User
from jose import jwt

from services.token import create_access_token, create_refresh_token
from transaction import Transaction


def get_token(user_id: int) -> BaseTokenDto:
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    return BaseTokenDto(**{
        "access_token": access_token,
        "refresh_token": refresh_token
    })


class LoginService:

    def __init__(self, user_repo: Annotated[UserRepository, Depends()], transaction: Annotated[Transaction, Depends()]):
        self.user_repository = user_repo
        self.transaction = transaction

    def handle_login(self, access_token: str, login_method: str) -> BaseTokenDto:
        if login_method == "KAKAO":
            user_id = self.request_kakao_user_info(access_token)
            return get_token(user_id)
        else:
            raise Exception("Invalid login method")

    def request_kakao_user_info(self, access_token: str) -> int:
        request_url = "https://kapi.kakao.com/v2/user/me"
        res = httpx.post(request_url, headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        })
        if res.status_code != HTTPStatus.OK:
            raise HTTPException(status_code=401)
        res_body: kakaologinapi.GetUserInfo = res.json()
        social_id = res_body['id']
        social_provider = SocialProvider.KAKAO
        user = self.user_repository.find_by_social_provider_and_social_id(social_provider=social_provider,
                                                                          social_id=str(social_id))
        if user is None:
            nickname = res_body['kakao_account']['profile']['nickname']
            user = User(social_provider=social_provider, social_id=social_id, nickname=nickname)
            with self.transaction:
                self.user_repository.create_or_update(user)

        return user.id
