from services.token import create_access_token, decode_access_token, create_refresh_token, decode_refresh_token


def test_create_access_token_and_decode_access_token():
    user_id = 1
    access_token = create_access_token(user_id)
    assert user_id == decode_access_token(access_token)


def test_create_refresh_token_and_decode_refresh_token():
    user_id = 1
    refresh_token = create_refresh_token(user_id)
    assert user_id == decode_refresh_token(refresh_token)

