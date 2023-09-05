from fastapi.exceptions import HTTPException


class RecordNotFoundException(Exception):
    """Raised when a record is not found"""


class RecordNotFoundHTTPException(HTTPException):
    def __init__(self, status_code=404, detail="Record not found") -> None:
        super().__init__(status_code, detail=detail)


class AWSConfigException(Exception):
    """Raised when there's a problem with aws config"""

    def __init__(self, detail: str):
        self.detail = detail


class AWSConfigExceptionHTTPException(HTTPException):
    def __init__(self, status_code=404, detail="AWS Error") -> None:
        super().__init__(status_code, detail=detail)


class AuthException(Exception):
    """Raised when there's a problem with jwt auth"""

    def __init__(self, detail: str):
        self.detail = detail


class AuthExceptionHTTPException(HTTPException):
    def __init__(self, status_code=401, detail="Auth Error") -> None:
        super().__init__(status_code, detail=detail)
