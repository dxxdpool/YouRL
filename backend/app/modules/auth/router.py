from app.core.database import get_db
from app.modules.auth.schemas import (
    UserRegisterRequest,
    UserResponse,
)
from app.modules.auth.service import register_user
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
