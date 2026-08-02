import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

try:
    import pyodbc
except ImportError:  # pragma: no cover - optional dependency for local DB access
    pyodbc = None

load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")
SERVER_NAME = os.getenv("SERVER_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")


def _build_engine():
    if DATABASE_URL:
        return create_engine(DATABASE_URL, future=True)

    if SERVER_NAME and DATABASE_NAME:
        connection_string = (
            f"mssql+pyodbc://{SERVER_NAME}/{DATABASE_NAME}"
            "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        )
        return create_engine(connection_string, future=True)

    raise RuntimeError(
        "No database configuration found. Set DATABASE_URL or SERVER_NAME + DATABASE_NAME in .env"
    )


engine = _build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_connection():
    if not pyodbc or not SERVER_NAME or not DATABASE_NAME:
        return None

    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER_NAME};"
        f"DATABASE={DATABASE_NAME};"
        f"Trusted_Connection=yes;"
    )

    try:
        return pyodbc.connect(connection_string)
    except Exception as exc:  # pragma: no cover - defensive logging
        print(exc)
        return None