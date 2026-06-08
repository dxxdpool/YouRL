from datetime import datetime
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from app.modules.urls.models import ShortURL


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    clicked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    url_id: Mapped[int] = mapped_column(
        ForeignKey("urls.id"),
        nullable=False,
    )

    url: Mapped["ShortURL"] = relationship(back_populates="analytics_events")
