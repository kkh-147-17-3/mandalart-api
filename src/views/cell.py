from typing import Annotated

from fastapi import Depends, Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models.cell import GetCellDto, UpdateCellDto, GetCellWithChildrenDto
from models.response import GenericResponse
from services.cell import CellService

router = InferringRouter()


@cbv(router)
class CellView:
    cell_service: CellService = Depends(CellService)

    @router.patch("/cell/{cell_id}", response_model=GenericResponse[GetCellDto],
                  summary="만다르트 셀 한 개의 내용을 수정합니다.", tags=["cell"],
                  description="셀의 수정하고자 하는 필드를 입력하여 셀 내용을 수정합니다. "
                              "입력된 필드의 내용만 수정되고, 입력되지 않은 필드는 수정하지 않습니다.")
    def update_cell(self, cell_id: int, dto: UpdateCellDto):
        user_id = 1
        result = self.cell_service.update_cell(dto, user_id, cell_id)
        return GenericResponse(status=200, data=result, message="Success")

    # @router.get("/cell/{cell_id}", response_model=GenericResponse[GetCellWithChildrenDto],
    #             summary="만다르트 셀 한 개의 정보를 가져옵니다.", tags=["cell"])
    # def get_cell(self, cell_id: int):
    #     user_id = 1
    #     result = self.cell_service.get_by_id(user_id, cell_id)
    #     return GenericResponse(status=200, data=result, message="Success")

    @router.get("/sheet/{sheet_id}/cell", response_model=GenericResponse[list[GetCellDto]],
                summary="만다르트 시트의 셀 9개를 불러옵니다.", tags=["sheet"])
    def get_sheet_cells(self, sheet_id: int,
                        depth: Annotated[int, Query(ge=1, le=2)],
                        parent_order: Annotated[int, Query(ge=0, le=7)] = 0):
        """
        return 중 `step_1_cell.children`은 step_1_cell 필드 내용과 동일
        """
        user_id = 1
        result = self.cell_service.get_by_sheet_id_and_depth_and_parent_order(user_id, sheet_id, depth, parent_order)
        return GenericResponse(status=200, data=result, message="Successfully fetched")
