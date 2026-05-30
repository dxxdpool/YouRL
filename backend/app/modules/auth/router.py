from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.auth.schemas import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.modules.auth.service import login_user, register_user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
async def register(
    data: UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await register_user(
        db,
        data,
    )

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    return await login_user(
        db,
        data,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user
