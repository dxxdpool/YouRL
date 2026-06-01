from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.urls.schemas import (
    CreateURLRequest,
    URLResponse,
)
from app.modules.urls.service import (
    create_short_url,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/urls",
    tags=["urls"],
)


@router.post(
    "",
    response_model=URLResponse,
)
async def create_url(
    data: CreateURLRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_short_url(
        db=db,
        current_user=current_user,
        data=data,
    )
