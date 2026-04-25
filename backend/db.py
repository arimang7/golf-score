import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings

# 프로젝트 루트 디렉토리 기준 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if settings.TURSO_URL and settings.TURSO_TOKEN:
    # Turso DB 연동 (libsql 드라이버 사용)
    db_url = settings.TURSO_URL
    if db_url.startswith("libsql://"):
        db_url = db_url.replace("libsql://", "sqlite+libsql://")
    
    SQLALCHEMY_DATABASE_URL = f"{db_url}?auth_token={settings.TURSO_TOKEN}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # 로컬 SQLite 파일 연동
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'golf_score.db')}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
