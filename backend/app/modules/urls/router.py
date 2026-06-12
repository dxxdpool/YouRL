from typing import Annotated

from app.core.database import get_db
from app.core.rate_limiter import rate_limit_create_url
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.urls.schemas import (
    CreateURLRequest,
    PaginatedURLsResponse,
    UpdateURLRequest,
    URLResponse,
)
from app.modules.urls.service import (
    create_short_url,
    delete_user_url,
    list_user_urls,
    update_user_url,
)
from fastapi import APIRouter, Depends, Query, status
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
    _: None = Depends(rate_limit_create_url),
):
    return await create_short_url(
        db=db,
        current_user=current_user,
        data=data,
    )


@router.get(
    "",
    response_model=PaginatedURLsResponse,
)
async def get_my_urls(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await list_user_urls(
        db,
        current_user,
        page,
        page_size,
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


@router.patch(
    "/{url_id}",
    response_model=URLResponse,
)
async def update_url_endpoint(
    url_id: int,
    data: UpdateURLRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await update_user_url(
        db,
        current_user,
        url_id,
        data,
    )
