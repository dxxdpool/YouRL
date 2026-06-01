from app.modules.auth.models import User
from app.modules.urls.repository import (
    create_url,
    get_url_by_short_code,
    get_url_by_user_and_original_url,
)
from app.modules.urls.schemas import (
    CreateURLRequest,
)
from app.modules.urls.utils import (
    generate_short_code,
)
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

    return await create_url(
        db,
        original_url=str(data.original_url),
        short_code=short_code,
        user_id=current_user.id,
    )
