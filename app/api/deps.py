from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.services.auth import AuthService
from app.common.exceptions import AuthExceptionHTTPException
from app.db.database import SessionLocal
from app.spot.services.spot_service import SpotService
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


security = HTTPBearer()


def hass_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
):
    if credentials:
        if not credentials.scheme == "Bearer":
            raise AuthExceptionHTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )
        if not auth_service.auth(token=credentials.credentials):
            raise AuthExceptionHTTPException(
                status_code=403, detail="Invalid token or expired token."
            )
        return credentials.credentials
    else:
        raise AuthExceptionHTTPException(status_code=403, detail="Invalid authorization code.")
