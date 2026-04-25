from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from backend.db import get_db
from backend.models.round import Round, RoundScore
from backend.models.user import User
from backend.auth_utils import get_current_user
from pydantic import BaseModel, Field

router = APIRouter(prefix="/rounds", tags=["rounds"])

class RoundCreate(BaseModel):
    course_id: int
    date: datetime
    players: List[str]

class HoleScoreUpdate(BaseModel):
    score_a: Optional[int] = Field(None, ge=-1, le=10)
    score_b: Optional[int] = Field(None, ge=-1, le=10)
    score_c: Optional[int] = Field(None, ge=-1, le=10)
    score_d: Optional[int] = Field(None, ge=-1, le=10)

@router.post("/")
def create_round(data: RoundCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 관리자 승인 확인
    if not current_user.is_approved:
        raise HTTPException(status_code=403, detail="승인된 사용자만 라운드를 생성할 수 있습니다.")

    # 골프장 정보 가져오기 (홀 수 확인용)
    from backend.models.course import GolfCourse
    course = db.query(GolfCourse).filter(GolfCourse.id == data.course_id).first()
    hole_count = course.holes if course else 18

    new_round = Round(
        course_id=data.course_id,
        date=data.date,
        players=data.players,
        created_by=current_user.id 
    )
    db.add(new_round)
    db.commit()
    db.refresh(new_round)
    
    # 골프장 홀 수만큼 초기화 (Bulk Insert)
    holes = [RoundScore(round_id=new_round.id, hole_number=i, par=4) for i in range(1, hole_count + 1)]
    db.add_all(holes)
    db.commit()
    
    return {
        "success": True, 
        "data": {
            "id": new_round.id,
            "course_id": new_round.course_id,
            "date": new_round.date,
            "players": new_round.players
        }
    }

@router.get("/")
def list_rounds(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_approved:
        return {"success": True, "data": [], "message": "승인 대기 중입니다."}

    # joinedload를 사용하여 N+1 문제 해결
    rounds = db.query(Round).options(joinedload(Round.course)).filter(Round.created_by == current_user.id).order_by(Round.date.desc()).all()
    
    results = []
    for r in rounds:
        results.append({
            "id": r.id,
            "course_id": r.course_id,
            "course_name": r.course.name if r.course else "Unknown",
            "date": r.date,
            "players": r.players
        })
    return {"success": True, "data": results}

@router.get("/{round_id}")
def get_round(round_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    round_data = db.query(Round).options(joinedload(Round.course)).filter(Round.id == round_id).first()
    if not round_data:
        raise HTTPException(status_code=404, detail="Round not found")
    
    if round_data.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    scores = [{"id": s.id, "hole_number": s.hole_number, "par": s.par, "score_a": s.score_a, "score_b": s.score_b, "score_c": s.score_c, "score_d": s.score_d} for s in round_data.scores]
    return {
        "success": True, 
        "data": {
            "id": round_data.id,
            "course_id": round_data.course_id,
            "course_name": round_data.course.name if round_data.course else "Unknown",
            "date": round_data.date,
            "players": round_data.players,
            "scores": scores
        }
    }

@router.patch("/{round_id}/holes/{hole_number}")
def update_hole_score(
    round_id: int, 
    hole_number: int, 
    data: HoleScoreUpdate, 
    par: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    round_data = db.query(Round).filter(Round.id == round_id).first()
    if not round_data:
        raise HTTPException(status_code=404, detail="Round not found")
        
    if round_data.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    hole = db.query(RoundScore).filter(
        RoundScore.round_id == round_id, 
        RoundScore.hole_number == hole_number
    ).first()
    
    if not hole:
        raise HTTPException(status_code=404, detail="Hole not found")
    
    if par is not None:
        hole.par = par
        
    # Pydantic 모델을 사용하여 명시적인 필드만 업데이트 (보안 강화)
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(hole, key, value)
            
    db.commit()
    db.refresh(hole)
    return {
        "success": True, 
        "data": {
            "id": hole.id,
            "hole_number": hole.hole_number,
            "par": hole.par,
            "score_a": hole.score_a,
            "score_b": hole.score_b,
            "score_c": hole.score_c,
            "score_d": hole.score_d
        }
    }
