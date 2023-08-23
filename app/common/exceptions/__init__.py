from fastapi.exceptions import HTTPException


class RecordNotFoundException(Exception):
    """Raised when a record is not found"""


class RecordNotFoundHTTPException(HTTPException):
    def __init__(self, status_code=404, detail="Record not found") -> None:
        super().__init__(status_code, detail=detail)
