import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings

# 프로젝트 루트 디렉토리 기준 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if settings.TURSO_URL and settings.TURSO_TOKEN:
    # Turso DB 연동 — 공식 권장 방식
    # URL 형식: sqlite+libsql://<hostname>?secure=true
    # 인증: connect_args에 auth_token 전달
    turso_url = settings.TURSO_URL  # libsql://golf-arimang7.aws-ap-northeast-1.turso.io
    SQLALCHEMY_DATABASE_URL = f"sqlite+{turso_url}?secure=true"

    # ── SQLite 방언의 PRAGMA 호출을 사전 차단 ──
    # Turso(Hrana 프로토콜)는 PRAGMA를 지원하지 않으므로 405 에러가 발생.
    from sqlalchemy.dialects.sqlite.base import SQLiteDialect

    def _patched_initialize(self, connection):
        self.get_isolation_level = lambda dbapi_conn: "AUTOCOMMIT"
        self.get_default_isolation_level = lambda dbapi_conn: "AUTOCOMMIT"
        self.set_isolation_level = lambda dbapi_conn, level: None
        self.default_isolation_level = "AUTOCOMMIT"
        self.default_schema_name = None
        self._broken_fk_pragma_quotes = False
        self._broken_dotted_colnames = False
        self.supports_default_values = True
        self.supports_default_metavalue = False
        self.supports_empty_insert = False
        self.supports_cast = True
        self.supports_multivalues_insert = True
        self.supports_statement_cache = True
        if not hasattr(self, 'server_version_info'):
            self.server_version_info = (3, 35, 0)
        self._is_oracle = False
    
    SQLiteDialect.initialize = _patched_initialize

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"auth_token": settings.TURSO_TOKEN},
        isolation_level=None,
        pool_pre_ping=False,
    )

    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        engine.dialect.get_isolation_level = lambda dbapi_conn: "AUTOCOMMIT"
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
