from app.modules.auth.models import User
from app.modules.urls.models import ShortURL
from app.modules.urls.repository import (
    create_url,
    delete_url,
    get_paginated_urls_by_user_id,
    get_total_urls_by_user_id,
    get_url_by_id_and_user_id,
    get_url_by_short_code,
    get_url_by_user_and_original_url,
)
from app.modules.urls.schemas import (
    CreateURLRequest,
    PaginatedURLsResponse,
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

    existing_url = await get_url_by_user_and_original_url(
        db,
        current_user.id,
        str(data.original_url),
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
