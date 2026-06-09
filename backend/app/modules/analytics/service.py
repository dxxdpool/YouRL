from app.modules.analytics.repository import (
    create_analytics_event,
)
from app.modules.urls.models import ShortURL
from sqlalchemy.ext.asyncio import AsyncSession


async def record_click(
    db: AsyncSession,
    url: ShortURL,
) -> None:

    try:
        await create_analytics_event(
            db,
            url.id,
        )

        url.click_count += 1

        await db.commit()

    except Exception:
        await db.rollback()
        raise
