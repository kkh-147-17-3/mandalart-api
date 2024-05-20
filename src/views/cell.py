from typing import Annotated

from fastapi import Depends, Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models.cell import GetCellDto, UpdateCellDto, GetCellWithTodosDto
from services.cell import CellService
from views.auth import AuthView

router = InferringRouter()


@cbv(router)
class CellView(AuthView):
    cell_service: CellService = Depends(CellService)

    @router.patch("/cell/{cell_id}", response_model=GetCellWithTodosDto,
                  summary="만다르트 셀 한 개의 내용을 수정합니다.", tags=["cell"],
                  description="셀의 수정하고자 하는 필드를 입력하여 셀 내용을 수정합니다. "
                              "입력된 필드의 내용만 수정되고, 입력되지 않은 필드는 수정하지 않습니다.")
    def update_cell(self, cell_id: int, dto: UpdateCellDto):
        user_id = self.user_id
        # user_id = 1
        return self.cell_service.update_cell(dto, user_id, cell_id)

    # @router.get("/cell/{cell_id}", response_model=GenericResponse[GetCellWithChildrenDto],
    #             summary="만다르트 셀 한 개의 정보를 가져옵니다.", tags=["cell"])
    # def get_cell(self, cell_id: int):
    #     user_id = 1
    #     result = self.cell_service.get_by_id(user_id, cell_id)
    #     return GenericResponse(status=200, data=result, message="Success")

    @router.get("/sheet/{sheet_id}/cell/main", response_model=list[GetCellDto],
                summary="만다르트 시트의 정 중앙에 있는 셀 9개를 불러옵니다.", tags=["sheet"])
    def get_sheet_cells(self, sheet_id: int):
        """
        return 중 `step_1_cell.children`은 step_1_cell 필드 내용과 동일
        """
        user_id = self.user_id
        return self.cell_service.get_by_sheet_id_and_depth_and_parent_order(user_id, sheet_id, 1, 0)

    @router.get("/cell/{cell_id}", summary="개별 셀 정보를 불러옵니다.", description="개별 셀의 정보를 불러옵니다. 하위 셀 정보는 포함하지 않습니다.",
                tags=['cell'])
    def get_cell_info(self, cell_id: int) -> GetCellWithTodosDto:
        return self.cell_service.get_by_id(self.user_id, cell_id)

    @router.get("/cell/{cell_id}/children", summary="특정 셀의 하위 셀 정보를 불러옵니다.", tags=['cell'])
    def get_cell_children(self, cell_id: int) -> list[GetCellDto]:
        return self.cell_service.get_children_cells_by_id(self.user_id, cell_id)

    @router.delete("/cell/{cell_id}", summary="cell 의 내용을 전부 삭제합니다(초기화).", tags=["cell"],
                   description="셀의 내용을 전부 삭제합니다. 해당 cell이 depth 2인 경우 하위 셀의 정보를 모두 초기화합니다.")
    def delete_cell(self, cell_id: int) -> GetCellWithTodosDto:
        return self.cell_service.delete_cell(self.user_id, cell_id)
