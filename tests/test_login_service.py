from unittest.mock import patch

import pytest

from models.token import BaseTokenDto
from repositories import UserRepository
from services.login import LoginService
from transaction import Transaction
from test_config import mock_db_session


@pytest.fixture
def mock_service(mock_db_session):
    user_repo = UserRepository(mock_db_session)
    transaction = Transaction(mock_db_session)
    return LoginService(user_repo, transaction)


# @p
def test_handle_kakao_login(mock_service):
    with patch.object(mock_service, "request_kakao_user_info", return_value=1):
        result = mock_service.handle_login(
            "test-kakao-access-token",
            "KAKAO")
        assert isinstance(result, BaseTokenDto)
