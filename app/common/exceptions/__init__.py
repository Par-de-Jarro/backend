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


class NotAvailableSpotVacanciesException(Exception):
    def __init__(self):
        super().__init__("Selected Spot has no vacancies available.")


class SpotEntryRequestAlreadyAccepted(Exception):
    def __init__(self):
        super().__init__("Request Already Accepted")


class SpotEntryRequestAlreadyDenied(Exception):
    def __init__(self):
        super().__init__("Request Already Denied")


class SpotEntryRequestAlreadyAcceptedHTTPException(HTTPException):
    def __init__(self, status_code=400, detail="Request Already Accepted") -> None:
        super().__init__(status_code, detail=detail)


class SpotEntryRequestAlreadyDeniedHTTPException(HTTPException):
    def __init__(self, status_code=400, detail="Request Already Denied") -> None:
        super().__init__(status_code, detail=detail)


class NotAvailableSpotVacanciesHTTPException(HTTPException):
    def __init__(self, status_code=400, detail="No vacancies") -> None:
        super().__init__(status_code, detail=detail)

class SpotHasNoOccupantsException(HTTPException):
    def __init__(self, status_code=400, detail="This spot has no associated occupants") -> None:
        super().__init__(status_code, detail=detail)
