from typing import override

from database import Base


class CustomException(Exception):

    def __init__(self, msg: str | None = None):
        self.msg = msg

    def __str__(self):
        return self.msg


class UnauthorizedException(CustomException):
    def __init__(self, msg: str = "not allowed to access data"):
        super().__init__(msg)
        self.msg = msg


class EntityNotFoundException(CustomException):
    def __init__(self, entity: Base | None = None, msg: str | None = None, **kwargs):
        super().__init__(msg)
        self.entity = entity
        self.lookup_fields = kwargs

    def __str__(self):
        return self.msg if self.msg else (f"Entity not found {f"- [{self.entity.__table__}]" if self.entity else ""} "
                                          f"{f": lookup fields: {self.lookup_fields}" if self.lookup_fields else ""}")


class MissingEnvVarException(CustomException):
    pass
