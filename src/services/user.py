from typing import Annotated

from fastapi import Depends

from errors.exceptions import EntityNotFoundException
from models.user import UserDto
from repositories import UserRepository
from schemas import User


class UserService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends()]):
        self.user_repo = user_repo

    def get_user_info(self, user_id: int) -> UserDto:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise EntityNotFoundException(User, user_id=user_id)

        return UserDto(**user.__dict__)
