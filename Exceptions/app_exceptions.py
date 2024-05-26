class BaseAppException(Exception):
    def __init__(self, msg: str = ""):
        self.msg = msg
        super().__init__(self.msg)


class TransactionException(BaseAppException):
    pass
