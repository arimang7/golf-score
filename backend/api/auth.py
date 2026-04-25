from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.db import get_db
from backend.models.user import User
from backend.auth_utils import create_access_token, decode_access_token
from backend.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

class VoiceTextRequest(BaseModel):
    text: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class UserApprovalRequest(BaseModel):
    user_id: int
    is_approved: bool

@router.post("/admin/login")
async def admin_login(data: AdminLoginRequest, db: Session = Depends(get_db)):
    if data.username == settings.ADMIN_USERNAME and data.password == settings.ADMIN_PASSWORD:
        try:
            user = db.query(User).filter(User.email == "admin@internal").first()
            if not user:
                user = User(
                    google_id="admin_manual",
                    email="admin@internal",
                    name="System Administrator",
                    is_admin=True,
                    is_approved=True
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            
            access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
            from fastapi.responses import JSONResponse
            response = JSONResponse(content={"message": "Admin logged in", "success": True})
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                samesite="lax",
                secure=True # Vercel (HTTPS) 환경을 위해 추가
            )
            return response
        except Exception as e:
            # DB 연동 등의 에러가 발생할 경우 500 에러의 원인을 상세히 반환
            raise HTTPException(status_code=500, detail=f"Database or Server Error: {str(e)}")
    
    raise HTTPException(status_code=401, detail="Invalid admin credentials")

@router.get("/users")
async def list_users(request: Request, db: Session = Depends(get_db)):
    # 관리자 여부 확인 (간단한 구현)
    token = request.cookies.get("access_token")
    if not token: raise HTTPException(status_code=401)
    payload = decode_access_token(token)
    current_user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
        
    users = db.query(User).all()
    return {"success": True, "data": users}

@router.post("/users/approve")
async def approve_user(data: UserApprovalRequest, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token: raise HTTPException(status_code=401)
    payload = decode_access_token(token)
    current_user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    user = db.query(User).filter(User.id == data.user_id).first()
    if not user: raise HTTPException(status_code=404)
    
    user.is_approved = data.is_approved
    db.commit()
    return {"success": True}

@router.get("/google/login")
async def login(request: Request):
    # 개발 환경과 배포 환경 구분
    # Vercel은 보통 https를 사용하므로 X-Forwarded-Proto 등을 참조할 수도 있지만
    # 가장 안전한 방법은 request.url_for를 그대로 쓰는 것입니다.
    redirect_uri = request.url_for('auth_callback')
    
    # 만약 Vercel 내부 라우팅 문제로 http로 잡힌다면 강제로 https로 변경
    redirect_str = str(redirect_uri)
    if "vercel.app" in redirect_str and redirect_str.startswith("http://"):
        redirect_str = redirect_str.replace("http://", "https://")
        
    return await oauth.google.authorize_redirect(request, redirect_str)

@router.get("/google/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google authentication failed: {str(e)}")
    
    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info from Google")

    # DB에서 사용자 확인 및 생성
    try:
        user = db.query(User).filter(User.google_id == user_info['sub']).first()
        if not user:
            # 첫 번째 유저라면 관리자로 자동 지정 (옵션)
            user_count = db.query(User).count()
            is_initial_admin = user_count == 0
            
            user = User(
                google_id=user_info['sub'],
                email=user_info['email'],
                name=user_info.get('name'),
                picture_url=user_info.get('picture'),
                is_admin=is_initial_admin,
                is_approved=is_initial_admin
            )
            db.add(user)
            db.commit()
            db.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error during user creation: {str(e)}")

    # JWT 토큰 발급
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    
    # 프론트엔드로 리다이렉트 (Vercel 도메인 판단)
    import os
    is_vercel = os.getenv("VERCEL") == "1"
    
    host = request.headers.get("x-forwarded-host") or request.headers.get("host", "")
    protocol = request.headers.get("x-forwarded-proto", "https" if is_vercel else "http")
    
    # 확실하게 프로덕션 환경인지 체크
    is_production = is_vercel or "vercel.app" in host or ("localhost" not in host and "127.0.0.1" not in host)
    
    if is_production:
         # 배포된 환경이라면 HTTPS 강제 및 현재 호스트 사용
         redirect_target = f"https://{host}/"
    else:
         redirect_target = "http://localhost:5173/"

    response = RedirectResponse(url=redirect_target)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=True if protocol == "https" else False
    )
    return response

@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out", "success": True}

@router.get("/me")
async def get_me(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture_url": user.picture_url,
            "is_approved": user.is_approved,
            "is_admin": user.is_admin
        }, 
        "success": True
    }
