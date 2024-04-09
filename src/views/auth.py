from fastapi import Depends

from services.token import auth_access_wrapper


class AuthView:
    user_id: int = Depends(auth_access_wrapper)
