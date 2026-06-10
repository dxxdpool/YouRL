from datetime import UTC, datetime

from app.modules.auth.models import User
from app.modules.urls.models import ShortURL
from app.modules.urls.repository import (
    create_url,
    delete_url,
    get_existing_url,
    get_paginated_urls_by_user_id,
    get_total_urls_by_user_id,
    get_url_by_id_and_user_id,
    get_url_by_short_code,
)
from app.modules.urls.schemas import (
    CreateURLRequest,
    PaginatedURLsResponse,
    UpdateURLRequest,
)
from app.modules.urls.utils import (
    generate_short_code,
)
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


async def create_short_url(
    db: AsyncSession,
    current_user: User,
    data: CreateURLRequest,
):
    if data.expires_at is not None and data.expires_at <= datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expiration time must be in the future",
        )

    existing_url = await get_existing_url(
        db,
        current_user.id,
        str(data.original_url),
        data.expires_at,
    )

    if existing_url:
        return existing_url

    while True:

        short_code = generate_short_code()

        collision = await get_url_by_short_code(
            db,
            short_code,
        )

        if not collision:
            break

    try:
        url = await create_url(
            db,
            original_url=str(data.original_url),
            short_code=short_code,
            user_id=current_user.id,
            expires_at=data.expires_at,
        )

        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(url)

    return url


async def get_url(
    db: AsyncSession,
    short_code: str,
) -> ShortURL:

    url = await get_url_by_short_code(
        db,
        short_code,
    )

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )

    if url.expires_at is not None and datetime.now(UTC) >= url.expires_at:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="URL has expired",
        )

    return url


async def list_user_urls(
    db: AsyncSession,
    current_user: User,
    page: int,
    page_size: int,
) -> PaginatedURLsResponse:

    offset = (page - 1) * page_size

    urls = await get_paginated_urls_by_user_id(
        db,
        current_user.id,
        offset,
        page_size,
    )

    total = await get_total_urls_by_user_id(
        db,
        current_user.id,
    )

    return PaginatedURLsResponse(
        items=urls,
        total=total,
        page=page,
        page_size=page_size,
    )


async def delete_user_url(
    db: AsyncSession,
    current_user: User,
    url_id: int,
) -> None:

    url = await get_url_by_id_and_user_id(
        db,
        url_id,
        current_user.id,
    )

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )

    try:
        await delete_url(
            db,
            url,
        )

        await db.commit()
    except Exception:
        await db.rollback()
        raise


async def update_user_url(
    db: AsyncSession,
    current_user: User,
    url_id: int,
    data: UpdateURLRequest,
) -> ShortURL:

    url = await get_url_by_id_and_user_id(
        db,
        url_id,
        current_user.id,
    )

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )

    if data.expires_at is not None and data.expires_at <= datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expiration time must be in the future",
        )

    existing_url = await get_existing_url(
        db,
        current_user.id,
        url.original_url,
        data.expires_at,
    )

    if existing_url and existing_url.id != url.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("A URL with the same destination and expiration already exists"),
        )

    try:
        url.expires_at = data.expires_at

        await db.commit()
        await db.refresh(url)

        return url

    except Exception:
        await db.rollback()
        raise
