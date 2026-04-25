import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings

# 프로젝트 루트 디렉토리 기준 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if settings.TURSO_URL and settings.TURSO_TOKEN:
    # Turso DB 연동 (libsql 드라이버 사용)
    clean_url = settings.TURSO_URL.replace("libsql://", "").replace("https://", "").replace("http://", "").strip("/")
    SQLALCHEMY_DATABASE_URL = f"sqlite+libsql://{clean_url}?auth_token={settings.TURSO_TOKEN}"

    # Vercel 환경의 Turso 연결 안정성을 위한 엔진 설정
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        # SQLAlchemy가 연결 시 격리 수준을 확인하기 위해 PRAGMA 명령을 날리는 것을 방지
        isolation_level=None,
        pool_pre_ping=False, # ping도 연결 초기에 에러를 유발할 수 있으므로 제거
        execution_options={"isolation_level": "AUTOCOMMIT"} # 명시적인 트랜잭션 관리 방지
    )
    
    # 더 강력하게 PRAGMA 실행 방지 (SQLite 방언 객체의 동작 강제 수정)
    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        # 방언(Dialect)의 isolation_level 관련 메서드를 빈 함수로 교체하여 PRAGMA 쿼리 차단
        if hasattr(engine.dialect, 'get_isolation_level'):
            engine.dialect.get_isolation_level = lambda dbapi_conn: "AUTOCOMMIT"
        if hasattr(engine.dialect, 'set_isolation_level'):
            engine.dialect.set_isolation_level = lambda dbapi_conn, level: None
            
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
