from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class HealthCheckResponse(BaseModel):
    """Schema for the health check response."""

    status: str
    message: str


class URLrequest(BaseModel):
    """Schema for the incoming request to shorten a URL."""

    url: HttpUrl
    expiry_days: Optional[int] = None


class URLResponse(BaseModel):
    """Schema for the outgoing response after a URL is shortened."""

    short_code: str
    short_url: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: Optional[datetime] = None


class StatsResponse(BaseModel):
    """Schema for the statistics response."""

    model_config = ConfigDict(from_attributes=True)

    short_code: str
    original_url: str
    click_count: int
    created_at: datetime
    expires_at: Optional[datetime] = None