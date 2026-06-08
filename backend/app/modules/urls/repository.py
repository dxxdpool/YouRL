from app.modules.urls.models import ShortURL
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_url_by_user_and_original_url(
    db: AsyncSession,
    user_id: int,
    original_url: str,
) -> ShortURL | None:

    result = await db.execute(
        select(ShortURL).where(
            ShortURL.user_id == user_id,
            ShortURL.original_url == original_url,
        )
    )

    return result.scalar_one_or_none()


async def get_url_by_short_code(
    db: AsyncSession,
    short_code: str,
) -> ShortURL | None:

    result = await db.execute(select(ShortURL).where(ShortURL.short_code == short_code))

    return result.scalar_one_or_none()


async def get_paginated_urls_by_user_id(
    db: AsyncSession,
    user_id: int,
    offset: int,
    limit: int,
) -> list[ShortURL]:

    result = await db.execute(
        select(ShortURL)
        .where(ShortURL.user_id == user_id)
        .order_by(ShortURL.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return list(result.scalars().all())


async def get_total_urls_by_user_id(
    db: AsyncSession,
    user_id: int,
) -> int:

    result = await db.execute(
        select(func.count(ShortURL.id)).where(ShortURL.user_id == user_id)
    )

    return result.scalar_one()


async def get_url_by_id_and_user_id(
    db: AsyncSession,
    url_id: int,
    user_id: int,
) -> ShortURL | None:

    result = await db.execute(
        select(ShortURL).where(
            ShortURL.id == url_id,
            ShortURL.user_id == user_id,
        )
    )

    return result.scalar_one_or_none()


async def create_url(
    db: AsyncSession,
    *,
    original_url: str,
    short_code: str,
    user_id: int,
) -> ShortURL:

    url = ShortURL(
        original_url=original_url,
        short_code=short_code,
        user_id=user_id,
    )

    db.add(url)

    return url


async def delete_url(
    db: AsyncSession,
    url: ShortURL,
) -> None:

    await db.delete(url)
