from unittest.mock import patch, MagicMock, PropertyMock

import pytest

from schemas.cell import Cell
from services import CellService
from test_config import client, mock_db_session
from views.cell import CellView


def test_get_user():
    res = client.get("/user/3")

    assert res.status_code == 200


def test_post_cell(mock_db_session):
    data = {
        'sheet_id': 1,
        'goal': 'test',
        'color': '#fff',
        'depth': 2,
        'order': 3,
        'parent_order': 1
    }
    mock_service = MagicMock(spec=CellService)
    mock_service.create_cell.return_value = \
        Cell(
            id=4,
            color=data['color'],
            goal=data['goal'],
            depth=data['depth'],
            order=data['order'],
            parent=Cell(
                depth=data['depth'] - 1,
                order=data['parent_order'],
                id=3,
                color='#fff',
                goal='test goal',
            )
        )
    with patch.object(CellView, 'cell_service', new_callable=PropertyMock, return_value=mock_service):
        # with patch.object(CellView, 'cell_service', new_callable=PropertyMock) as mock_cell_service:
        res = client.post("/cell", json=data)
        assert res.status_code == 200
        res_data = res.json()['data']
        assert res_data['color'] == data['color']
        assert res_data['goal'] == data['goal']
        assert res_data['order'] == data['order']
        assert res_data['depth'] == data['depth']
        assert res_data['parent']['order'] == data['parent_order']
        assert res_data['parent']['depth'] == data['depth'] - 1
