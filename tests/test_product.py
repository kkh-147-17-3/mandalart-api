import pytest
from .test_config import client


def test_endpoint():
    res = client.find_by_id("/user/3")

    assert res.status_code == 200
