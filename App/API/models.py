from database import Base
from sqlalchemy import Column, DateTime, Integer, String, Text


class HealthCheck(Base):
    __tablename__ = "HealthCheck"
    __table_args__ = {"schema": "URL", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(5))
    message = Column(String(20))


class Registry(Base):
    __tablename__ = "Registry"
    __table_args__ = {"schema": "URL", "extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_code = Column(String(10), unique=True, nullable=False)
    original_url = Column(Text, nullable=False)
    click_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=True)