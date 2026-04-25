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
            samesite="lax"
        )
        return response
    
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
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))

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

    # JWT 토큰 발급
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    
    # 프론트엔드로 리다이렉트
    response = RedirectResponse(url="http://localhost:5173")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
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
