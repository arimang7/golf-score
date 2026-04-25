# Par Score - AI Voice Golf Scorer

세련된 디자인과 음성 인식 기술을 결합한 골프 스코어 관리 애플리케이션입니다. 필드 위에서 번거로운 텍스트 입력 대신, 목소리만으로 4명의 점수를 실시간으로 기록할 수 있습니다.

## 🚀 주요 기능

- **음성 인식 스코어링**: 브라우저 내장 Web Speech API를 활용하여 "영, 일, 마이너스 일, 이"와 같이 숫자 나열만으로 4명의 점수를 즉시 기록.
- **상상 그 이상의 속도**: 숫자가 4개 감지되는 즉시 자동으로 분석 및 반영되는 실시간 처리 로직.
- **세련된 UI/UX**: Chiaroscuro(명암 대비) 레이아웃과 Rosso Corsa 레드 액센트를 활용한 프리미엄 디자인.
- **라운드 이력 관리**: 과거 라운드 기록을 한눈에 확인하고 상세 스코어카드를 조회.
- **관리자 승인 시스템**: 구글 로그인을 지원하며, 관리자의 승인을 받은 유저만 스코어카드 작성이 가능하도록 보안 강화.
- **골프장 데이터 자동 임포트**: 국내 주요 골프장 정보를 사전에 탑재하고, 필요시 직접 입력 가능.

## 🛠 Tech Stack

- **Frontend**: React (Vite), TailwindCSS, Lucide React, Zustand
- **Backend**: FastAPI (Python), SQLAlchemy, Pydantic
- **Database**: SQLite (Development)
- **Auth**: Google OAuth2 (Authlib), JWT
- **Voice**: Web Speech API (Native)

## ⚙️ 시작하기

### 1. 환경 설정

프로젝트 루트에 `.env.local` 파일을 생성하고 다음 정보를 입력합니다 (`.env.example` 참고):

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=golf1234
JWT_SECRET=your_secure_random_string
```

### 2. 백엔드 실행

```bash
# 가상환경 구축 및 패키지 설치
python -m venv venv
source venv/Scripts/activate # Windows
pip install -r backend/requirements.txt

# DB 초기화 및 골프장 데이터 시딩
python backend/init_db.py
python backend/seed_courses.py

# 서버 실행
python -m uvicorn backend.main:app --reload --port 8000
```

### 3. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173`으로 접속합니다.

## 👥 관리자 권한 (Admin)

- **초기 관리자**: `admin / golf1234` (backend/config.py에서 변경 가능)
- **유저 승인**: 관리자 계정으로 로그인 후 유저 목록에서 '사용 승인'을 클릭해야 일반 유저가 라운드를 시작할 수 있습니다.

## 📁 프로젝트 구조

```text
golf-score/
├── backend/                # FastAPI 서버
│   ├── api/                # API 엔드포인트 (Auth, Rounds, Courses, Voice)
│   ├── models/             # SQLAlchemy DB 모델
│   ├── services/           # 비즈니스 로직 (Voice Parser 등)
│   ├── main.py             # 앱 진입점 및 미들웨어 설정
│   └── requirements.txt    # 파이썬 의존성
├── frontend/               # React (Vite) 클라이언트
│   ├── src/
│   │   ├── api/            # API 클라이언트 (Axios)
│   │   ├── components/     # 재사용 컴포넌트 (HoleCard 등)
│   │   ├── pages/          # 페이지 컴포넌트 (Home, Login, Admin 등)
│   │   └── store/          # 상태 관리 (Zustand)
│   └── package.json        # 노드 의존성
├── db-src/                 # 초기 데이터 (골프장 현황 JSON)
├── review/                 # 코드 리뷰 기록
└── README.md
```

## 📝 라이선스

MIT License
