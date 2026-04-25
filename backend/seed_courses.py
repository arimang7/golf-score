import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import SessionLocal
from backend.models.course import GolfCourse

def seed():
    db = SessionLocal()
    
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db-src", "업종별골프장현황.json")
    
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        courses_data = json.load(f)
    
    print(f"Found {len(courses_data)} courses in JSON.")
    
    added_count = 0
    for c_data in courses_data:
        name = c_data.get("BIZPLC_NM")
        address = c_data.get("REFINE_ROADNM_ADDR") or c_data.get("REFINE_LOTNO_ADDR")
        holes = int(c_data.get("GOLFCRS_HOLE_CNT", 18))
        
        # 주소에서 지역 추출 (예: "경기도 여주시" -> "경기")
        region = "기타"
        if address:
            parts = address.split()
            if parts:
                region = parts[0][:2] # 경기도 -> 경기, 서울특별시 -> 서울
        
        if not name:
            continue

        # 중복 체크 (이름과 주소가 같은 경우)
        exists = db.query(GolfCourse).filter(
            GolfCourse.name == name,
            GolfCourse.address == address
        ).first()
        
        if not exists:
            course = GolfCourse(
                name=name,
                address=address,
                holes=holes,
                region=region
            )
            db.add(course)
            added_count += 1
            
            # 대량 데이터인 경우 중간 커밋
            if added_count % 50 == 0:
                db.commit()
    
    db.commit()
    db.close()
    print(f"Seeding complete! Added {added_count} new courses.")

if __name__ == "__main__":
    seed()
