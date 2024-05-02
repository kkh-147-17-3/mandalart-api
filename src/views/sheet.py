from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models.response import CreateSheetResponse
from models.sheet import CreateSheetDto, GetSheetInfoDto
from services.sheet import SheetService
from views.auth import AuthView

router = InferringRouter()


@cbv(router)
class SheetView(AuthView):
    sheet_service: SheetService = Depends(SheetService)

    @router.post("/sheet", summary="새로운 만다르트 시트를 생성합니다.", tags=["sheet"],
                 description="새 시트를 생성합니다. 생성 시 시트의 81개 셀을 모두 생성합니다.")
    def create_sheet(self, dto: CreateSheetDto) -> CreateSheetResponse:
        user_id = self.user_id
        created_sheet = self.sheet_service.create_sheet(dto, user_id)
        return CreateSheetResponse(**{
            'sheet_id': created_sheet.id
        })

    @router.get("/sheet/{sheet_id}",
                summary="가장 중앙의 만다르트 셀 정보를 포함한 만다르트 시트 정보를 불러옵니다.", tags=["sheet"])
    def get_sheet_info(self, sheet_id: int) -> GetSheetInfoDto:
        """
        return 중 `step_1_cell.children`은 step_1_cell 필드 내용과 동일
        """
        user_id = self.user_id
        return self.sheet_service.get_by_sheet_id(sheet_id, user_id)

    @router.get("/sheet", summary="시트 목록을 불러옵니다.", tags=["sheet"],
                description="나의 시트 id 목록을 불러옵니다. 가장 최근에 생성된 시트부터 내림차순으로 가져옵니다.")
    def get_my_sheet(self) -> list[int]:
        user_id = self.user_id
        sheets = self.sheet_service.get_by_user_id(user_id)
        return [sheet.id for sheet in sheets]
