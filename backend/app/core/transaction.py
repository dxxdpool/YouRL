from sqlalchemy.ext.asyncio import AsyncSession


async def commit_or_rollback(
    db: AsyncSession,
) -> None:
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
