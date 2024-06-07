from .cell import router as cell_router
from .healthcheck import router as healthcheck_router
from .sheet import router as sheet_router
from .user import router as user_router
from .token import router as token_router
from .login import router as login_router
from .todo import router as todo_router
from .oauth import router as oauth_router

routers = (
    cell_router,
    healthcheck_router,
    sheet_router,
    user_router,
    token_router,
    login_router,
    oauth_router
)
