from typing import TypedDict


class Partner(TypedDict):
    uuid: str | None


class Profile(TypedDict):
    nickname: str


class KakaoAccount(TypedDict):
    name: str
    profile: Profile


class GetUserInfo(TypedDict):
    id: int
    has_signed_up: bool | None
    connected_at: str | None
    synched_at: str | None
    properties: dict
    kakao_account: KakaoAccount
    partner: Partner
