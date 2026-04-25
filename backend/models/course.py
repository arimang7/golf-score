from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.db import Base

class GolfCourse(Base):
    __tablename__ = "golf_courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    address = Column(String)
    holes = Column(Integer, default=18)
    region = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
