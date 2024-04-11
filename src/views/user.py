from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models.user import UserDto
from services.user import UserService
from views.auth import AuthView

router = InferringRouter()


@cbv(router)
class UserView(AuthView):
    user_service: UserService = Depends(UserService)

    @router.get("/user/me", tags=["user"], summary="나의 정보를 불러옵니다.")
    def get_my_info(self) -> UserDto:
        return self.user_service.get_user_info(self.user_id)
