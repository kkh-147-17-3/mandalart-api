import os
from typing import Dict

from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory='src/templates')


@router.get("/")
async def healthcheck() -> Dict[str, str | None]:
    flag = os.environ.get("DEPLOYMENT_FLAG")
    return {
        "flag": flag
    }


@router.get("/login-page")
def get_login_page(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})
