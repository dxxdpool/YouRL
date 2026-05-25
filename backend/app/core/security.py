from datetime import datetime, timedelta, timezone

from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    user_id: int,
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
