from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import jwt

from enums import SocialProvider
from models.token import BaseTokenDto
import httpx
from models import kakaologinapi
from repositories import UserRepository
from schemas import User

from services.token import create_access_token, create_refresh_token, create_apple_client_secret
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

    def handle_apple_login(self, code: str, id_token: str):
        url = "https://appleid.apple.com/auth/token"
        data = {
            "client_id": "com.baker.eggtart.web",
            "code": code,
            "grant_type": "authorization_code",
            "client_secret": create_apple_client_secret(),
            "redirect_uri": "https://api.eggtart.in/login/apple"
        }
        res = httpx.post(url, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }, data=data)
        if res.status_code != 200:
            raise Exception("Login Failed")
        res_body = res.json()
        id_token = res_body['id_token']
        refresh_token = res_body['refresh_token']
        decoded_token = jwt.decode(id_token, options={'verify_signature': False})
        social_id = decoded_token['sub']
        social_provider = SocialProvider.APPLE
        user = self.user_repository.find_by_social_provider_and_social_id(social_provider=social_provider,
                                                                          social_id=str(social_id))
        if user is None:
            nickname = decoded_token['name']
            user = User(social_provider=social_provider,
                        social_id=social_id,
                        nickname=nickname,
                        apple_refresh_token=refresh_token)
            with self.transaction:
                self.user_repository.create_or_update(user)

        return user.id
