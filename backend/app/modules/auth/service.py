from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.modules.auth.models import User
from app.modules.auth.repository import (
    create_user,
    get_user_by_email,
)
from app.modules.auth.schemas import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


async def register_user(
    db: AsyncSession,
    data: UserRegisterRequest,
) -> User:

    existing_user = await get_user_by_email(
        db,
        data.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    password_hash = hash_password(data.password)

    user = await create_user(
        db,
        email=data.email,
        password_hash=password_hash,
    )

    return user


async def login_user(
    db: AsyncSession,
    data: UserLoginRequest,
) -> TokenResponse:

    user = await get_user_by_email(
        db,
        data.email,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    valid_password = verify_password(
        data.password,
        user.password_hash,
    )

    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(user.id)

    return TokenResponse(
        access_token=access_token,
    )
