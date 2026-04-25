from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.db import get_db
from backend.models.course import GolfCourse
from pydantic import BaseModel

router = APIRouter(prefix="/courses", tags=["courses"])

class CourseCreate(BaseModel):
    name: str
    address: Optional[str] = None
    holes: int = 18
    region: Optional[str] = None

@router.get("/")
def search_courses(query: Optional[str] = Query(None), db: Session = Depends(get_db)):
    db_query = db.query(GolfCourse)
    if query:
        # 간단한 검색 구현 (이름 또는 지역)
        db_query = db_query.filter(
            (GolfCourse.name.contains(query)) | (GolfCourse.region.contains(query))
        )
    return {"success": True, "data": db_query.all()}

@router.post("/")
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    # 이름 중복 체크 (선택 사항)
    existing = db.query(GolfCourse).filter(GolfCourse.name == data.name).first()
    if existing:
        # 이미 존재하면 해당 코스 반환하거나 에러
        return {"success": True, "data": existing, "message": "Already exists"}
        
    new_course = GolfCourse(
        name=data.name,
        address=data.address,
        holes=data.holes,
        region=data.region or (data.address[:2] if data.address else "기타")
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"success": True, "data": new_course}

@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(GolfCourse).filter(GolfCourse.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Golf course not found")
    return {"success": True, "data": course}
