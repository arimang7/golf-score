# Code Review Results - Golf Score Service

본 문서는 `code-reviewer` 에이전트를 통해 수행된 주요 코드 리뷰 결과와 이에 따른 조치 사항을 기록합니다.

## 🚨 1. 보안 및 아키텍처 (Critical)

### A. Mass Assignment 취약점 (`backend/api/rounds.py`)
- **문제점**: `update_hole_score` 엔드포인트에서 `dict` 형태의 데이터를 검증 없이 `setattr`로 모델에 직접 반영하고 있었습니다. 공격자가 `id`나 `round_id` 같은 시스템 필드를 주입하여 데이터를 조작할 위험이 있었습니다.
- **조치 사항**: Pydantic 모델(`HoleScoreUpdate`)을 도입하여 `score_a`~`score_d` 등 허용된 필드만 명시적으로 업데이트하도록 수정했습니다.

### B. 비즈니스 로직 중복 (DRY 원칙 위배)
- **문제점**: 한국어 숫자 매핑 로직(`kor_num_map`)과 정규표현식이 프론트엔드(`HoleCard.jsx`)와 백엔드(`voice_parser.py`) 양쪽에 중복 구현되어 유지보수가 어려웠습니다.
- **조치 사항**: 백엔드를 단일 진실 공급원(Single Source of Truth)으로 설정했습니다. 프론트엔드에서는 텍스트만 서버로 전달하고, 모든 파싱 및 보정 로직은 백엔드에서 통합 관리하도록 구조를 개선했습니다.

## ⚠️ 2. 성능 및 안정성 (Important)

### A. N+1 쿼리 성능 문제 (`backend/api/rounds.py`)
- **문제점**: 라운드 목록 조회(`list_rounds`) 시 SQLAlchemy의 Lazy Loading으로 인해 각 라운드마다 골프장 정보를 조회하는 추가 쿼리가 발생했습니다.
- **조치 사항**: `joinedload(Round.course)`를 사용하여 단 한 번의 Join 쿼리로 모든 정보를 가져오도록 최적화했습니다.

### B. 음성 인식 매핑 오탐지 가능성 (`backend/services/voice_parser.py`)
- **문제점**: 숫자가 감지되지 않을 때 글자 단위로 매핑하는 로직이 너무 공격적이어서, "정말"의 "정"을 0으로 인식하는 등의 오탐지 위험이 있었습니다.
- **조치 사항**: 단어 경계 및 숫자 유효 범위 필터링을 강화하여 오탐지를 최소화했습니다.

## 💡 3. 코드 품질 및 유지보수 (Suggestions)

### A. 대량 데이터 삽입 (Bulk Insert)
- **조치 사항**: `create_round` 시 18번의 루프를 돌며 개별적으로 저장하던 방식을 `db.add_all()`을 사용한 일괄 삽입 방식으로 변경하여 성능을 개선했습니다.

### B. 레이스 컨디션 방지
- **조치 사항**: 프론트엔드의 음성 인식 결과 처리 로직에 `isProcessing` 가드를 추가하여, 서버 응답이 오기 전에 중복 요청이 발생하는 것을 방지했습니다.

---
**Review Date**: 2026-04-25
**Reviewer**: Gemini CLI (Code-Reviewer Agent)
