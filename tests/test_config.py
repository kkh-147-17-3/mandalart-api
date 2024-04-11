from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest
from main import app
from dependencies import get_db
from services.token import auth_access_wrapper


def override_get_db():
    try:
        yield mock_session
    finally:
        pass


def override_auth_access_wrapper():
    return 1


@pytest.fixture
def mock_db_session():
    return mock_session


mock_session = MagicMock()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[auth_access_wrapper] = override_auth_access_wrapper

client = TestClient(app)
