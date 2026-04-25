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

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )

    # Vercel(Turso) 환경에서 PRAGMA 명령어로 인한 405 에러 방지
    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        # sqlite3 모듈의 cursor 객체를 몽키패치하여 특정 PRAGMA를 무시하도록 처리
        original_cursor = dbapi_connection.cursor
        def _mocked_cursor(*args, **kwargs):
            cursor = original_cursor(*args, **kwargs)
            original_execute = cursor.execute
            def _mocked_execute(sql, *a, **k):
                if "PRAGMA read_uncommitted" in sql:
                    return cursor
                return original_execute(sql, *a, **k)
            cursor.execute = _mocked_execute
            return cursor
        dbapi_connection.cursor = _mocked_cursor

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
