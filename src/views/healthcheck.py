import os

from fastapi import APIRouter

from models.response import GenericResponse

router = APIRouter()


@router.get("/")
async def healthcheck() -> GenericResponse[str]:
    flag = os.environ.get("DEPLOYMENT_FLAG")
    return GenericResponse(status=200, data="OK", message=flag)
