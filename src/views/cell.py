from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models.cell import CreateCellDto, GetCellDto, UpdateCellDto
from models.response import GenericResponse
from services.cell import CellService

router = InferringRouter()


@cbv(router)
class CellView:
    cell_service: CellService = Depends(CellService)

    @router.post("/cell", response_model=GenericResponse[GetCellDto],
                 summary="만다르트의 한 개의 셀을 생성합니다.",
                 tags=["cell"])
    def create_cell(self, dto: CreateCellDto):
        """
        depth: 1(정중앙), 2(정중앙에서 주위 8 개),3(depth=2 8개 셀 주변에 있는 8개의 셀)\n
        order \n
        |1|2|3|\n
        |4|X|5|\n
        |6|7|8|\n
        * depth: 1인 경우, order 는 무조건 1 \n
        color: hex code (ex: #fff, #FFF, #ffffff 모두 가능)
        """
        user_id = 1
        result = self.cell_service.create_cell(dto, user_id)
        return GenericResponse(status=200, data=result, message="Success")

    @router.put("/cell/{cell_id}", response_model=GenericResponse[GetCellDto],
                summary="만다르트 셀 한 개의 내용을 수정합니다.", tags=["cell"])
    def update_cell(self, cell_id: int, dto: UpdateCellDto):
        user_id = 1
        result = self.cell_service.update_cell(dto, user_id, cell_id)
        return GenericResponse(status=200, data=result, message="Success")
