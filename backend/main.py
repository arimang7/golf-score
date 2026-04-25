from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from backend.api import auth, courses, rounds, voice
from backend.config import settings
from backend.db import engine, Base
# 모든 모델을 import하여 Base.metadata에 등록
from backend.models.user import User
from backend.models.course import GolfCourse
from backend.models.round import Round, RoundScore
import uvicorn

app = FastAPI(title="Golf Score API")

# Turso DB인 경우 테이블 자동 생성 (서버리스 환경에서 필수)
@app.on_event("startup")
async def startup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[WARN] Table creation skipped or failed: {e}")

# Vercel 등 프록시 환경에서 클라이언트 IP, 스킴(HTTPS), 호스트를 올바르게 인식하도록 설정
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])

# Authlib 세션 관리를 위한 미들웨어
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(rounds.router)
app.include_router(voice.router)

@app.get("/")
async def root():
    return {"message": "Golf Score API is running", "success": True}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
