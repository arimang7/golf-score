from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from backend.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    picture_url = Column(String)
    is_approved = Column(Boolean, default=False) # 관리자 승인 여부
    is_admin = Column(Boolean, default=False)    # 관리자 여부
    created_at = Column(DateTime(timezone=True), server_default=func.now())
