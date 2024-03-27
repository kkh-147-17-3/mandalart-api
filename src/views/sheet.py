from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models.response import GenericResponse
from models.sheet import CreateSheetDto, GetSheetDto, GetSheetInfoDto
from services.sheet import SheetService

router = InferringRouter()


@cbv(router)
class SheetView:
    sheet_service: SheetService = Depends(SheetService)

    @router.post("/sheet", response_model=GenericResponse[GetSheetDto], summary="새로운 만다르트 시트를 생성합니다.", tags=["sheet"])
    def create_sheet(self, dto: CreateSheetDto):
        user_id = 1
        result = self.sheet_service.create_sheet(dto, user_id)
        return GenericResponse(status=200, data=result, message="Successfully created")

    @router.get("/sheet/{sheet_id}", response_model=GenericResponse[GetSheetInfoDto],
                summary="가장 중앙의 만다르트 셀 정보를 포함한 만다르트 시트 정보를 불러옵니다.", tags=["sheet"])
    def get_sheet_info(self, sheet_id: int):
        """
        return 중 `depth_1_cell.children`은 depth_1_cell 필드 내용과 동일
        """
        user_id = 1
        result = self.sheet_service.get_by_sheet_id(sheet_id, user_id)
        return GenericResponse(status=200, data=result, message="Successfully fetched")
