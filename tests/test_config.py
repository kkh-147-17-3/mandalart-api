from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest
from main import app
from dependencies import get_db


def override_get_db():
    try:
        yield mock_session
    finally:
        pass


@pytest.fixture
def mock_db_session():
    return mock_session


mock_session = MagicMock()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
