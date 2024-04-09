from database import Base


class UnauthorizedException(Exception):
    msg: str

    def __init__(self, msg: str = "not allowed to access data"):
        self.msg = msg

    def __str__(self):
        return self.msg


class EntityNotFoundException(Exception):
    def __init__(self, entity: Base | None, **kwargs):
        self.entity = entity
        self.lookup_fields = kwargs

    def __str__(self):
        return (f"Entity not found {f"- [{self.entity.__table__}]" if self.entity else ""} "
                f"{f": lookup fields: {self.lookup_fields}" if self.lookup_fields else ""}")
