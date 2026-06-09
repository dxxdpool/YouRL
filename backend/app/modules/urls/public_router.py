from app.core.database import get_db
from app.modules.analytics.service import record_click
from app.modules.urls.service import get_url
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/r/{short_code}")
async def redirect_url(
    short_code: str,
    db: AsyncSession = Depends(get_db),
):
    url = await get_url(
        db,
        short_code,
    )

    await record_click(
        db,
        url,
    )

    return RedirectResponse(
        url=url.original_url,
        status_code=307,
    )
