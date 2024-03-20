import pytest
from .test_config import client


def test_새로운_유저_생성():
    res = client.get_by_id("/user/3")

    assert res.status_code == 200
