from app.core.security import hash_password
from app.modules.auth.models import User
from app.modules.auth.repository import (
    create_user,
    get_user_by_email,
)
from app.modules.auth.schemas import (
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
