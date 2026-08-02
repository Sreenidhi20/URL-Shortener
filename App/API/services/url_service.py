from datetime import datetime, timedelta, timezone
from typing import Optional

from config import DEFAULT_EXPIRY_DAYS
from fastapi import HTTPException, status
from models import Registry
from sqlalchemy.orm import Session
from utils.short_code import generate_short_code

MAX_GENERATION_ATTEMPTS = 5


def create_short_url(
    db: Session,
    original_url: str,
    expiry_days: Optional[int] = None,
) -> Registry:
    """Create a new short URL entry in the database."""
    if expiry_days is None:
        expiry_days = DEFAULT_EXPIRY_DAYS

    expires_at = datetime.now(timezone.utc) + timedelta(days=expiry_days)

    for _ in range(MAX_GENERATION_ATTEMPTS):
        short_code = generate_short_code()
        existing_entry = db.query(Registry).filter_by(short_code=short_code).first()
        if existing_entry is None:
            new_entry = Registry(
                short_code=short_code,
                original_url=original_url,
                created_at=datetime.now(timezone.utc),
                expires_at=expires_at,
            )
            db.add(new_entry)
            db.commit()
            db.refresh(new_entry)
            return new_entry

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to generate a unique short code after multiple attempts.",
    )


def get_mapping_or_404(db: Session, short_code: str) -> Registry:
    """Retrieve a URL mapping by its short code or raise a 404 error."""
    mapping = db.query(Registry).filter_by(short_code=short_code).first()
    if mapping is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found.")
    return mapping


def _as_aware_utc(dt: datetime) -> datetime:
    """Convert a naive datetime to an aware UTC datetime."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def resolve_and_increment_click_count(db: Session, short_code: str) -> Registry:
    """Resolve a short code to its original URL and increment the click count."""
    mapping = get_mapping_or_404(db, short_code)

    if mapping.expires_at and _as_aware_utc(datetime.now()) > _as_aware_utc(mapping.expires_at):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Short code has expired.")

    mapping.click_count += 1
    db.commit()
    db.refresh(mapping)

    return mapping


def delete_mapping(db: Session, short_code: str) -> None:
    """Delete a URL mapping by its short code."""
    mapping = get_mapping_or_404(db, short_code)
    db.delete(mapping)
    db.commit()