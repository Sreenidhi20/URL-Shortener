from database import get_db
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from schemas import StatsResponse, URLrequest, URLResponse
from services import url_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["urls"])
redirect_router = APIRouter(tags=["redirects"])


@router.get("", include_in_schema=False)
def api_root() -> dict[str, object]:
    return {
        "message": "URL shortener API",
        "endpoints": ["/api/shorten", "/api/stats/{short_code}"],
    }


@router.options("/shorten", include_in_schema=False)
def preflight_shorten() -> Response:
    return Response(status_code=200)


@router.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(
    payload: URLrequest,
    request: Request,
    db: Session = Depends(get_db),
) -> URLResponse:
    """Create a short URL entry and return its public link."""
    new_entry = url_service.create_short_url(db, str(payload.url), payload.expiry_days)
    base_url = str(request.base_url).rstrip("/")
    short_url = f"{base_url}/{new_entry.short_code}"
    return URLResponse(
        short_code=new_entry.short_code,
        short_url=short_url,
        original_url=new_entry.original_url,
        created_at=new_entry.created_at,
        expires_at=new_entry.expires_at,
    )


@redirect_router.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)) -> RedirectResponse:
    mapping = url_service.resolve_and_increment_click_count(db, short_code)
    return RedirectResponse(url=mapping.original_url)


@router.get("/stats/{short_code}", response_model=StatsResponse)
def get_url_stats(short_code: str, db: Session = Depends(get_db)) -> StatsResponse:
    return url_service.get_mapping_or_404(db, short_code)


@router.delete("/{short_code}", status_code=204)
def delete_short_url(short_code: str, db: Session = Depends(get_db)) -> None:
    url_service.delete_mapping(db, short_code)