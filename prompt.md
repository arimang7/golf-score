# Golf Score 기록 및 통계 모바일 웹 앱 개발

## 1. 프로젝트 개요

스마트폰 구글 브라우저에서 사용하는 골프 스코어 기록·통계 웹앱.
사용자는 최대 4인(A,B,C,D)이 함께 라운드하며 음성으로 스코어를 입력할 수 있다.

---

## 2. 기술 스택

### Backend

- Runtime: Python 3.12+
- Framework: FastAPI
- DB: Turso - SQLite3 (SQLAlchemy ORM + Alembic 마이그레이션)
- Auth: Google OAuth2 (authlib 또는 python-social-auth)
- 음성 처리: SpeechRecognition + Google Speech-to-Text API (또는 openai-whisper local)
- 자연어 파싱: 정규식 기반 파서 (예: "1번홀 파4 A 스코어 5, B 스코어 4" → 구조화된 JSON)
- 서버: Uvicorn (로컬), Vercel serverless (배포 시 Python runtime 사용)

### Frontend

- React 18 + Vite
- 상태관리: Zustand
- 스타일: Tailwind CSS v3
- 라우터: React Router v6
- HTTP: axios
- 음성 녹음: ~~MediaRecorder API (브라우저 내장) → Blob을 백엔드로 전송~~
  - 가장 빠르고 가벼운 선택: Web Speech API
    별도의 라이브러리 설치 없이 브라우저 자체 기능을 사용하는 방식입니다. 모바일 크롬에서 가장 안정적으로 작동합니다.

          특징: 구글의 서버 기반 인식을 사용하므로 한국어 인식률이 매우 높고 가볍습니다.

          장점: 추가 용량 없음, 무료, 구현이 매우 간단함.

          단점: 인터넷 연결이 필수적이며, 골프장처럼 데이터가 불안정한 곳에서는 끊길 수 있습니다.

          추천 라이브러리: annyang

          Web Speech API를 래핑하여 "1번 홀 4타" 같은 **음성 명령(Command)**을 매핑하기 매우 쉽습니다.

          annyang.addCommands({'*hole번 홀 *score타': myFunc}) 식으로 직관적인 코딩이 가능합니다.

- UI 컴포넌트: shadcn/ui (모바일 최적화 기준)
- PWA: vite-plugin-pwa (오프라인 지원 고려)

### 인프라

- 버전관리: GitHub
- 배포: Vercel (Frontend + Python Backend serverless functions)
- DB 파일: Vercel Blob Storage 또는 Railway SQLite 볼륨 (Vercel은 파일시스템 휘발성 주의 → 명시적 설명 필요)
- CI/CD: GitHub Actions → Vercel 자동 배포

---

## 3. 데이터베이스 스키마

### users

- id (PK), google_id (UNIQUE), email, name, picture_url, created_at

### golf_courses

- id (PK), name, address, holes (default 18), region, created_at
- 초기 데이터: 한국 주요 골프장 50개 이상 seed

### rounds

- id (PK), course_id (FK), date, players (JSON: ["A","B","C","D"]), created_by (FK→users), created_at

### round_scores

- id (PK), round_id (FK), hole_number (1~18), par (3~5)
- score_a, score_b, score_c, score_d (NULL 허용 - 참가 인원 가변)
- voice_transcript (TEXT, 원본 음성 텍스트 저장)

---

## 4. API 설계 (FastAPI)

### Auth

- GET /auth/google/login → Google OAuth 리다이렉트
- GET /auth/google/callback → 토큰 발급, JWT 쿠키 세팅
- POST /auth/logout → 쿠키 삭제
- GET /auth/me → 현재 사용자 정보

### 골프장

- GET /courses?query={검색어} → 골프장 검색 (이름/지역)
- GET /courses/{id} → 골프장 상세

### 라운드

- POST /rounds → 라운드 생성 (course_id, date, players 배열)
- GET /rounds → 내 라운드 목록
- GET /rounds/{id} → 라운드 상세 (전체 홀 스코어 포함)
- PATCH /rounds/{id}/holes/{hole_number} → 특정 홀 스코어 수동 수정
- DELETE /rounds/{id} → 라운드 삭제

### 음성 입력

- POST /rounds/{id}/holes/{hole_number}/voice
  - Body: multipart/form-data (audio_file: .webm or .wav)
  - 처리: STT → 자연어 파서 → DB 저장 → 파싱 결과 JSON 반환
  - 반환: { hole: 1, par: 4, scores: {A:5, B:4, C:5, D:5}, transcript: "..." }

### 통계

- GET /stats/me → 내 통계
  - 반환: 평균 스코어, 베스트 라운드, 파 대비 +/-, 홀별 평균, 최근 10라운드 트렌드

---

## 5. 음성 파싱 로직

백엔드 파서 구현 요구사항:

```python
# 입력 예시 transcript:
# "1번홀 파4 A 스코어 5 B 스코어 4 C 스코어 5 D 스코어 5"
# "3번홀 파3 에이 4 비 3 씨 5"  ← 한국어 발음 변형 처리
# "파이브 홀 파4 A5 B4"         ← 축약형 처리

# 파서가 추출해야 할 정보:
# - hole_number: 1~18
# - par: 3, 4, 5
# - scores: {A: int, B: int, C: int, D: int} (참여 플레이어만)

# 처리 규칙:
# - 한국어 숫자: 일=1, 이=2, 삼=3, 사=4, 오=5, 육=6, 칠=7, 팔=8, 구=9
# - 영어 발음: one,two,three... → 변환
# - A/에이, B/비, C/씨, D/디 모두 인식
# - 파싱 실패 시 {"error": "파싱 실패", "transcript": "..."} 반환 → 프론트에서 수동 입력 유도
```

---

## 6. 프론트엔드 화면 구성 (모바일 우선)

### 공통

- Bottom Navigation Bar: 홈, 라운드, 통계, 프로필 (4탭)
- 최대 너비 430px 중앙 정렬, 배경 그린/화이트 골프 테마

### 화면 목록

#### /login

- 구글 로그인 버튼 (Google Sign-In 공식 버튼 스타일 준수)

#### /home (/)

- 최근 라운드 3개 요약 카드
- 새 라운드 시작 CTA 버튼
- 핸디캡/평균 스코어 뱃지

#### /courses/search

- 검색창 (debounce 300ms)
- 골프장 목록 카드 (이름, 지역, 홀수)
- 선택 → 라운드 생성 플로우로 이동

#### /rounds/new

- 골프장 선택됨 표시
- 날짜 선택 (date picker)
- 플레이어 선택 (A,B,C,D 토글 버튼, 최소 1인)
- 생성 버튼

#### /rounds/{id}

- 상단: 골프장명, 날짜, 플레이어 표시
- 홀 카드 리스트 (1~18홀 세로 스크롤)
  - 각 홀 카드: 홀번호, PAR 선택(3/4/5), 플레이어별 스코어 입력 (+/- 버튼)
  - 🎤 음성 입력 버튼: 누르는 동안 녹음 (push-to-talk 방식)
    - 녹음 중: 빨간 pulse 애니메이션
    - 전송 중: 로딩 스피너
    - 성공: 자동으로 스코어 채워짐 + 진동(vibrate API)
    - 실패: 토스트 에러 + 수동 입력 활성화
  - 스코어 컬러 코딩: 버디(파란색), 파(흰색/회색), 보기(주황색), 더블보기+(빨간색)
- 하단: 현재까지 합계 스코어 실시간 표시

#### /rounds/{id}/summary

- 라운드 완료 후 전체 스코어카드 (테이블)
- 전반/후반/합계 행
- 각 플레이어 파 대비 점수(+/-)
- 공유 버튼 (Web Share API → 이미지 캡처 후 공유)

#### /stats

- 필터: 기간(1개월/3개월/6개월/전체), 플레이어(A/B/C/D)
- 차트: 최근 라운드 스코어 트렌드 (Recharts LineChart)
- 홀별 평균 스코어 바 차트
- 요약 카드: 총 라운드수, 평균 스코어, 베스트 스코어, 이글/버디/파/보기 카운트

#### /profile

- 구글 프로필 사진, 이름, 이메일
- 로그아웃 버튼

---

## 7. 프로젝트 구조

golf-score-app/
├── backend/
│ ├── main.py # FastAPI app entry
│ ├── api/
│ │ ├── auth.py
│ │ ├── courses.py
│ │ ├── rounds.py
│ │ ├── stats.py
│ │ └── voice.py
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic schemas
│ ├── services/
│ │ ├── voice_parser.py # STT + 자연어 파서
│ │ └── stats_service.py
│ ├── db.py # DB 세션
│ ├── auth.py # JWT + Google OAuth
│ ├── seed_courses.py # 골프장 초기 데이터
│ └── requirements.txt
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── HoleCard.jsx
│ │ │ ├── VoiceInput.jsx
│ │ │ ├── ScoreInput.jsx
│ │ │ └── BottomNav.jsx
│ │ ├── pages/
│ │ │ ├── Login.jsx
│ │ │ ├── Home.jsx
│ │ │ ├── CourseSearch.jsx
│ │ │ ├── RoundNew.jsx
│ │ │ ├── RoundDetail.jsx
│ │ │ ├── RoundSummary.jsx
│ │ │ ├── Stats.jsx
│ │ │ └── Profile.jsx
│ │ ├── store/ # Zustand stores
│ │ ├── api/ # axios API 함수
│ │ └── App.jsx
│ ├── index.html
│ ├── vite.config.js
│ └── package.json
├── vercel.json # 라우팅 설정
└── .github/
└── workflows/
└── ci.yml

---

## 8. 개발 순서 (단계별 진행)

**Phase 1 - 기반 구축**

1. FastAPI 프로젝트 초기화 + SQLAlchemy 모델 + Alembic 마이그레이션
2. Google OAuth2 로그인/로그아웃 + JWT 미들웨어
3. 골프장 CRUD API + 시드 데이터
4. React + Vite 초기화 + Tailwind + shadcn/ui + React Router
5. 로그인 페이지 + Auth 컨텍스트

**Phase 2 - 핵심 기능** 6. 라운드 생성/조회 API + 화면 7. 홀 스코어 입력 UI (HoleCard, ScoreInput) 8. 음성 입력 파이프라인 (MediaRecorder → 백엔드 STT → 파서 → 화면 반영) 9. 라운드 요약 화면

**Phase 3 - 통계 및 마무리** 10. 통계 API + Recharts 차트 11. PWA 설정 (vite-plugin-pwa, manifest.json) 12. Vercel 배포 설정 (vercel.json, 환경변수) 13. GitHub Actions CI/CD 파이프라인

---

## 9. 환경변수 목록

- end.local 사용

## 10. 추가 구현 요구사항

- 모든 API 응답: `{ success: bool, data: any, message: str }` 통일 형식
- 음성 입력 실패 시 수동 입력 fallback 반드시 제공
- 스코어 입력 중 페이지 이탈 방지 (beforeunload 경고)
- 홀 카드는 현재 입력 중인 홀이 자동 스크롤 포커스
- 접근성: aria-label 필수 (특히 음성 버튼)
- 에러 처리: 네트워크 오류 시 로컬스토리지 임시 저장 후 재시도
- 골프장 검색은 한국어 초성 검색 지원 (예: "ㅅㅇ" → 서원힐스)

모든 코드는 한국어 주석 포함. 타입 힌트(Python) 및 PropTypes(React) 필수 적용.

## 11. 추가 요건

1.db-src의 "업종별골프장현황.json"를 골프장 기본 정보에 저장 2.골프장은 사용자가 key-in으로 추가할 수 있게 3.스코어 녹음 mock 대신 실제 마이크로 입력하게 수정 (현재 notebook mic 연결 완료)
4.scorecard 저장시 녹음 버튼을 각 홀 번호 옆에 추가해서 몇번 홀인지 얘기하지 않게

- 녹음 방식 :
  1. 각 홀 번호 옆 녹음 버튼 클릭
  2. 예) 순서대로 0,1,-1,2
     par bogey birddy double
  3. 종료 버튼 클릭

  5.scorecard 입력 개수는 par개수 대비 입력하는 것이라서, 즉 par 4홀에서 4개 쳤으면 par인거고 홀의 스코어는 0으로 입력
  6.scorecard의 합산은 입력한 숫자의 합산, 입력한 숫자 + par의 개수의 합산 으로 두가지 방식으로 상단에 표현
  7.scorecard 저장 및 이력관리 기능 추가
  8.admin 권한 관리 추가 - google login을 해도 권한 부여를 해야지 scorecard를 쓸 수 있음

  9.README.md 최신화
  10.git push를 위해 민감 정보 분리, .gitignore반영
  11.code-review skill을 이용한 코드 리뷰
  12.vercel 배포를 위한 준비
