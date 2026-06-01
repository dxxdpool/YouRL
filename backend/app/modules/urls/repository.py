from app.modules.urls.models import ShortURL
from sqlalchemy import select
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

    await db.commit()
    await db.refresh(url)

    return url
