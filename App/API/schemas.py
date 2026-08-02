from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, field_validator


class HealthCheckResponse(BaseModel):
    """Schema for the health check response."""

    status: str
    message: str


class URLrequest(BaseModel):
    """Schema for the incoming request to shorten a URL."""

    url: str
    expiry_days: Optional[int] = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("URL cannot be empty")

        if "://" not in cleaned_value:
            cleaned_value = f"https://{cleaned_value}"

        parsed_url = urlparse(cleaned_value)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Please provide a valid URL")

        return cleaned_value


class URLResponse(BaseModel):
    """Schema for the outgoing response after a URL is shortened."""

    short_code: str
    short_url: str
    original_url: str
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