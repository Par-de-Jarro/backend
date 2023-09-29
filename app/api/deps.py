from fastapi import Depends, Request, Security
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.services.auth import AuthService
from app.common.exceptions import AuthExceptionHTTPException
from app.core.settings import API_TOKEN_AUTH_PASSWORD
from app.db.database import SessionLocal
from app.google.services.google import GoogleService
from app.spot.services.spot_service import SpotService
from app.university.services.university_service import UniversityService
from app.user.services.user_service import UserService


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:  # noqa: E722
        db.rollback()
        raise
    else:
        if db.is_active:
            db.commit()
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


def get_spot_service(db: Session = Depends(get_db)):
    return SpotService(db)


def get_auth_service(user_service: UserService = Depends(get_user_service)):
    return AuthService(user_service=user_service)


def get_university_service(db: Session = Depends(get_db)):
    return UniversityService(db)


def get_google_service():
    return GoogleService()


security = HTTPBearer()


async def get_id_user_by_auth_token(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    auth_token = request.headers.get("Authorization").split(" ")[1]
    auth_user = auth_service.auth(token=auth_token)

    return auth_user.id_user


def get_request_object(request: Request):
    return request


def token_auth():
    api_token_auth_header = APIKeyHeader(
        name="Api-Key",
        auto_error=False,
    )

    async def validate_token(
        api_token: str = Security(api_token_auth_header),
        request: Request = Depends(get_request_object),
    ):
        if "Api-Key" in request.headers:
            if api_token == API_TOKEN_AUTH_PASSWORD:
                return
        raise AuthExceptionHTTPException

    return validate_token


def hass_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
):
    if credentials:
        if not credentials.scheme == "Bearer":
            raise AuthExceptionHTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )

        auth_user = auth_service.auth(token=credentials.credentials)

        if not auth_user:
            raise AuthExceptionHTTPException(
                status_code=403, detail="Invalid token or expired token."
            )

        return auth_user
    else:
        raise AuthExceptionHTTPException(status_code=403, detail="Invalid authorization code.")
