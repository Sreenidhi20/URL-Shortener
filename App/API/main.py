import sys
from pathlib import Path

from database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import health, sql_health, url

API_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = API_DIR.parent.parent

for path in (str(API_DIR), str(PROJECT_ROOT)):
    if path not in sys.path:
        sys.path.append(path)

init_db()

app = FastAPI(
    title="URL Shortener API",
    description="A minimal, production-shaped URL shortener built with FastAPI + SQL Server.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the URL Shortener API!"}


app.include_router(health.router)
app.include_router(sql_health.router)
app.include_router(url.router)
app.include_router(url.redirect_router)