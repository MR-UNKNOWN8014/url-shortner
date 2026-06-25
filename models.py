from pydantic import BaseModel, HttpUrl

class ShortenRequest(BaseModel):
    original_url: HttpUrl

class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str

class URLStats(BaseModel):
    original_url: str
    short_code: str
    click_count: int