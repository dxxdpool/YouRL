from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.urls.schemas import (
    CreateURLRequest,
    URLResponse,
)
from app.modules.urls.service import create_short_url, delete_user_url, list_user_urls
from fastapi import APIRouter, Depends, status
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


@router.get(
    "",
    response_model=list[URLResponse],
)
async def get_my_urls(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await list_user_urls(
        db,
        current_user,
    )


@router.delete(
    "/{url_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_url_endpoint(
    url_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await delete_user_url(
        db,
        current_user,
        url_id,
    )
