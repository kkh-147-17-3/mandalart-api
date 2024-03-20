from typing import Annotated

from fastapi import Depends
from fastapi_oauth2.middleware import User

from enums import SocialProvider
from repositories import UserRepository


class TokenService:
    user_repository: UserRepository

    def __init__(self, user_repository: Annotated[UserRepository, Depends()]):
        self.user_repository = user_repository

    def get_token(self, oauth2_user: User) -> str:
        social_provider_id = str(oauth2_user.id)
        social_provider = SocialProvider[oauth2_user.provider.upper()]

        user = self.user_repository.get_user_by_social_id_and_provider(social_provider_id, social_provider)

        return social_provider_id
