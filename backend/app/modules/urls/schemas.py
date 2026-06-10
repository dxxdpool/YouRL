from datetime import datetime

from pydantic import BaseModel, HttpUrl


class CreateURLRequest(BaseModel):
    original_url: HttpUrl
    expires_at: datetime | None = None


class UpdateURLRequest(BaseModel):
    expires_at: datetime | None


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime
    expires_at: datetime | None

    model_config = {"from_attributes": True}


class PaginatedURLsResponse(BaseModel):
    items: list[URLResponse]
    total: int
    page: int
    page_size: int
