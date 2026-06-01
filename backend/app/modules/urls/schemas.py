from pydantic import BaseModel, HttpUrl


class CreateURLRequest(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str

    model_config = {"from_attributes": True}
