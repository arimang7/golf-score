from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.db import Base

class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("golf_courses.id"))
    date = Column(DateTime, nullable=False)
    players = Column(JSON, nullable=False)  # ["A", "B", "C", "D"]
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    course = relationship("GolfCourse")
    creator = relationship("User")
    scores = relationship("RoundScore", back_populates="round", cascade="all, delete-orphan")

class RoundScore(Base):
    __tablename__ = "round_scores"

    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, ForeignKey("rounds.id"))
    hole_number = Column(Integer, nullable=False)  # 1~18
    par = Column(Integer, default=4)
    score_a = Column(Integer, nullable=True)
    score_b = Column(Integer, nullable=True)
    score_c = Column(Integer, nullable=True)
    score_d = Column(Integer, nullable=True)
    voice_transcript = Column(String, nullable=True)

    round = relationship("Round", back_populates="scores")
