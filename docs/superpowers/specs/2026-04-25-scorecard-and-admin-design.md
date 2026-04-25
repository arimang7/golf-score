# Spec: Scorecard Storage, History & Admin Permission Management

- **Date:** 2026-04-25
- **Topic:** 스코어카드 저장/이력 관리 및 관리자 권한 제어 구현
- **Status:** Pending Review

## 1. Background & Goals
본 프로젝트는 골프 라운드 기록을 음성으로 입력하고 관리하는 서비스입니다. Vercel 배포와 함께 클라우드 데이터베이스(Turso)로의 전환이 필요하며, 사용자가 Google 로그인을 하더라도 관리자의 승인 없이는 기능을 사용할 수 없도록 보안을 강화하는 것이 핵심 목표입니다.

## 2. Technical Architecture: Database Switching
로컬 개발 환경과 배포 환경을 유연하게 전환하기 위해 `libsql`을 활용한 자동 전환 로직을 구현합니다.

- **Dependencies:** `libsql-experimental` 추가
- **Logic (`backend/db.py`):**
    - `TURSO_URL` 및 `TURSO_TOKEN` 환경변수 존재 시: `sqlite+libsql://` 프로토콜을 사용하여 Turso DB 연동
    - 환경변수 부재 시: 로컬 `sqlite:///golf_score.db` 파일 사용
- **Configuration:** `.env.local`에 Turso 관련 변수 관리

## 3. Database Schema & Migration
- **Models:**
    - `User`: `is_approved` (승인 여부), `is_admin` (관리자 여부) 필드 유지 및 검증 로직 강화
    - `Round` & `RoundScore`: 사용자별 이력 조회를 위해 `created_by` 외래키 관계 유지
- **Migration:**
    - Alembic을 사용하여 Turso DB에 테이블 스키마 생성 (`alembic upgrade head`)
    - `backend/seed_courses.py`를 실행하여 초기 골프장 데이터 적재

## 4. Admin Permission Flow
사용자 권한 관리를 위한 8번 요건을 다음과 같이 구현합니다.

- **Authentication:** Google OAuth2 로그인 성공 후, `is_approved`가 `False`인 유저는 서비스 이용이 제한됨
- **Backend Protection:**
    - `backend/api/rounds.py`의 모든 쓰기/조회 API에서 `current_user.is_approved` 체크 의존성(Dependency) 강화
    - 승인되지 않은 요청에 대해 `403 Forbidden` 반환
- **Frontend Experience:**
    - `Home.jsx`: 승인 대기 유저에게 경고 배너 노출 및 '새 라운드 시작' 버튼 숨김
    - `Admin.jsx`: 관리자가 유저 목록을 확인하고 승인 상태를 즉시 변경할 수 있는 UI 제공

## 5. Implementation Steps
1. **Dependency Update:** `requirements.txt`에 `libsql-experimental` 추가 및 설치
2. **Database Engine Update:** `backend/db.py`의 `create_engine` 로직 수정
3. **API Logic Review:** `backend/api/rounds.py`의 권한 체크 로직 전수 점검
4. **Frontend UI Polish:** `Home.jsx` 및 `Admin.jsx`에서 권한 상태에 따른 UI 처리 보강
5. **Verification:** 로컬 SQLite 환경과 Turso DB 환경 각각에서 정상 작동 여부 테스트

## 6. Self-Review
- **Placeholder scan:** TBD 없음. 모든 설정값은 환경변수에서 로드함.
- **Consistency:** `is_approved` 필드를 통해 백엔드와 프론트엔드에서 일관되게 권한을 제어함.
- **Scope check:** Turso 전환과 권한 관리 강화라는 명확한 범위에 집중함.
