from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from models.cell import CreateCellDto, GetCellDto
from models.response import GenericResponse
from services.cell import CellService

router = InferringRouter()


@cbv(router)
class CellView:
    cell_service: CellService = Depends(CellService)

    @router.post("/cell", response_model=GenericResponse[GetCellDto])
    def create_cell(self, dto: CreateCellDto):
        result = self.cell_service.create_cell(dto)
        return GenericResponse(status=200, data=result, message="Success")
