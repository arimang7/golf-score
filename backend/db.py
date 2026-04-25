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

    # ── SQLite 방언의 PRAGMA 호출을 사전 차단 ──
    # SQLAlchemy의 SQLite 방언은 dialect.initialize() → get_default_isolation_level()
    # → PRAGMA read_uncommitted 순서로 최초 연결 시 PRAGMA를 실행한다.
    # Turso(Hrana 프로토콜)는 PRAGMA를 지원하지 않으므로 405 에러가 발생.
    # connect 이벤트는 initialize() 이후에 실행되므로 너무 늦다.
    # → 방언 클래스 자체를 엔진 생성 전에 패치해야 한다.
    from sqlalchemy.dialects.sqlite.base import SQLiteDialect

    def _patched_initialize(self, connection):
        # 원래 initialize()는 PRAGMA read_uncommitted 등을 실행하므로 완전 우회.
        # 필요한 방언 속성만 수동 설정한다.
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

    # Vercel 환경의 Turso 연결 안정성을 위한 엔진 설정
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        isolation_level=None,
        pool_pre_ping=False,
    )

    # 연결 후에도 안전하게 PRAGMA 차단 유지
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
