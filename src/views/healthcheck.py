import os
from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def healthcheck() -> Dict[str, str | None]:
    flag = os.environ.get("DEPLOYMENT_FLAG")
    return {
        "flag": flag
    }
