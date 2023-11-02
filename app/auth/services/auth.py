from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt
from pydantic import ValidationError

from app.auth.schemas import AuthResponse, SessionCreate, TokenPayload
from app.common.exceptions import AuthException, AuthExceptionHTTPException, RecordNotFoundException
from app.common.utils.password import check_password
from app.core.settings import JWT_REFRESH_SECRET_KEY, JWT_SECRET_KEY
from app.user.schemas.user import UserSearchParams
from app.user.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
        self.ALGORITHM = "HS256"
        self.JWT_REFRESH_SECRET_KEY = JWT_REFRESH_SECRET_KEY
        self.JWT_SECRET_KEY = JWT_SECRET_KEY

    def auth(self, token: str):
        try:
            payload = jwt.decode(token, self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
            exp = datetime.fromtimestamp(payload["exp"])
            del payload["exp"]
            token_data = TokenPayload(**payload, exp=exp)

            if token_data.exp < datetime.now():
                raise AuthExceptionHTTPException(
                    status_code=401,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return self.user_service.get_by_id(id_user=UUID(token_data.id_user))

        except (jwt.JWTError, ValidationError, RecordNotFoundException):
            raise AuthExceptionHTTPException(
                status_code=403,
                detail="Could not validate credentials",
            )

    def create_tokens(self, session_create: SessionCreate) -> AuthResponse:
        users = self.user_service.get_all(UserSearchParams(email=session_create.email))

        if not users:
            raise AuthException(detail="User not registered")

        user = users[0]

        if not (check_password(session_create.password, user.password_hash)):
            raise AuthException(detail="Wrong password")

        return AuthResponse(
            access_token=self.create_access_token(user=user),
            refresh_token=self.create_refresh_token(user=user),
            user=user,
        )

    def create_access_token(self, user) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = TokenPayload(
            exp=expires_delta,
            sub=str(user.id_user),
            id_user=str(user.id_user),
            email=user.email,
            name=user.name,
        ).dict()

        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, self.ALGORITHM)

        return encoded_jwt

    def create_refresh_token(self, user) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = TokenPayload(
            exp=expires_delta,
            sub=str(user.id_user),
            id_user=str(user.id_user),
            email=user.email,
            name=user.name,
        ).dict()

        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, self.ALGORITHM)

        return encoded_jwt
