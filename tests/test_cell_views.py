from unittest.mock import patch, MagicMock, PropertyMock


from schemas.cell import Cell
from services import CellService
from test_config import client, mock_db_session
from views.cell import CellView


def test_update_cell(mock_db_session):
    mock_service = MagicMock(spec=CellService)
    mock_user_id = MagicMock(spec=int)

    cell_id = 1001

    data = {
        'goal': "test123",
        'color': "FFFFFFFF",
        'is_completed': False
    }
    mock_service.update_cell.return_value = Cell(
        id=cell_id,
        goal="test123",
        color="FFFFFFFF",
        is_completed=False
    )

    mock_user_id.return_value = 1

    with (
        patch.object(CellView, 'cell_service', new_callable=PropertyMock, return_value=mock_service),
    ):
        # with patch.object(CellView, 'cell_service', new_callable=PropertyMock) as mock_cell_service:
        res = client.patch(f"/cell/{cell_id}", json=data)
        assert res.status_code == 200
        res_data = res.json()['data']
        assert res_data['color'] == data['color']
        assert res_data['goal'] == data['goal']
        assert res_data['id'] == cell_id
