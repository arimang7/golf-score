# Scorecard Storage, History & Admin Permission Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turso DB 전환을 지원하고, 관리자 승인 여부에 따른 권한 제어를 백엔드와 프론트엔드 전반에 걸쳐 강화합니다.

**Architecture:** `libsql-experimental`을 사용하여 환경변수 존재 여부에 따라 로컬 SQLite와 Turso DB를 동적으로 전환합니다. 모든 라운드 관련 API에 승인 여부 체크 의존성을 추가합니다.

**Tech Stack:** FastAPI, SQLAlchemy, LibSQL, React (Vite)

---

### Task 1: Update Dependencies

**Files:**
- Modify: `backend/requirements.txt`

- [ ] **Step 1: Add `libsql-experimental` to `requirements.txt`**
- [ ] **Step 2: Install updated dependencies**
    Run: `pip install -r backend/requirements.txt`
- [ ] **Step 3: Commit**

---

### Task 2: Update Config & Database Engine

**Files:**
- Modify: `backend/config.py`
- Modify: `backend/db.py`

- [ ] **Step 1: `backend/config.py`에 `TURSO_URL`, `TURSO_TOKEN` 추가**
- [ ] **Step 2: `backend/db.py` 수정**
    `settings.TURSO_URL`이 있을 경우 `sqlite+libsql://` 형태로 연결 문자열 생성 및 엔진 생성 로직 추가.
- [ ] **Step 3: Commit**

---

### Task 3: Enforce Admin Approval in API

**Files:**
- Modify: `backend/api/rounds.py`

- [ ] **Step 1: `get_approved_user` 의존성(Dependency) 추가**
    `current_user.is_approved`가 `False`일 경우 403 에러 반환.
- [ ] **Step 2: 모든 라운드 관련 엔드포인트에 적용**
    `create_round`, `list_rounds`, `get_round`, `update_hole_score`에 적용.
- [ ] **Step 3: Commit**

---

### Task 4: Polish Frontend UI

**Files:**
- Modify: `frontend/src/pages/Home.jsx`
- Modify: `frontend/src/pages/Admin.jsx`

- [ ] **Step 1: `Home.jsx` UI 개선**
    승인 대기 중일 때의 메시지를 강조하고, 불필요한 UI 요소 비활성화.
- [ ] **Step 2: `Admin.jsx` 권한 관리 로직 확인**
    승인/취소 버튼 동작 및 실시간 반영 확인.
- [ ] **Step 3: Commit**

---

### Task 5: Verification & Seeding

- [ ] **Step 1: 로컬 SQLite 환경 테스트**
- [ ] **Step 2: Turso DB 연결 및 마이그레이션 테스트**
    `alembic upgrade head` 실행 확인.
- [ ] **Step 3: 초기 데이터 적재**
    `python -m backend.seed_courses` 실행 확인.
- [ ] **Step 4: Commit**
