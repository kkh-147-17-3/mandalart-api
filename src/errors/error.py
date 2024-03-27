class UnauthorizedError(Exception):
    msg: str

    def __init__(self, msg:str = "not allowed to access data"):
        self.msg = msg

    def __str__(self):
        return self.msg