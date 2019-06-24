
class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class ParserError(BaseException):
    pass

class EmptyContent(BaseException):
    pass

class ContainerNotFound(BaseException):
    pass

class RequestError(BaseException):
    pass