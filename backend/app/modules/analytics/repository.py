from app.modules.analytics.models import AnalyticsEvent
from sqlalchemy.ext.asyncio import AsyncSession


async def create_analytics_event(
    db: AsyncSession,
    url_id: int,
) -> AnalyticsEvent:

    event = AnalyticsEvent(
        url_id=url_id,
    )

    db.add(event)

    return event
