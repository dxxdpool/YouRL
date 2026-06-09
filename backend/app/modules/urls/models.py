from datetime import datetime, UTC
from typing import TYPE_CHECKING

from app.core.database import Base
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    from app.modules.analytics.models import AnalyticsEvent
    from app.modules.auth.models import User


class ShortURL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)

    original_url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    short_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    click_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="urls")

    analytics_events: Mapped[list["AnalyticsEvent"]] = relationship(
        back_populates="url",
        passive_deletes=True,
    )
