from app.core.database import get_db
from app.modules.urls.service import (
    get_original_url,
)
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/r/{short_code}")
async def redirect_url(
    short_code: str,
    db: AsyncSession = Depends(get_db),
):
    original_url = await get_original_url(
        db,
        short_code,
    )

    return RedirectResponse(
        url=original_url,
        status_code=307,
    )
