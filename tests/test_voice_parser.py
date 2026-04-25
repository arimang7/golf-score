"""voice_parser.py 단독 테스트"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.voice_parser import parse_voice_text, mock_stt

PASS = 0
FAIL = 0

def check(label, result, expected):
    global PASS, FAIL
    ok = result == expected
    mark = "PASS" if ok else "FAIL"
    if not ok:
        FAIL += 1
        print(f"  [{mark}] {label}")
        print(f"         got:      {result}")
        print(f"         expected: {expected}")
    else:
        PASS += 1
        print(f"  [{mark}] {label}")

print("=" * 60)
print("Voice Parser Unit Tests")
print("=" * 60)

# ── 1. 기본 케이스 ──────────────────────────────────────
print("\n[1] 기본: '1번홀 파4 A 스코어 5'")
r = parse_voice_text("1번홀 파4 A 스코어 5")
check("hole_number", r.get("hole_number"), 1)
check("par", r.get("par"), 4)
check("score_a", r["scores"].get("score_a"), 5)

# ── 2. 한글 플레이어 ────────────────────────────────────
print("\n[2] 한글: '3번홀 파5 에이 7타 비 스코어 6'")
r = parse_voice_text("3번홀 파5 에이 7타 비 스코어 6")
check("hole_number", r.get("hole_number"), 3)
check("par", r.get("par"), 5)
check("score_a", r["scores"].get("score_a"), 7)
check("score_b", r["scores"].get("score_b"), 6)

# ── 3. 4명 전부 ─────────────────────────────────────────
print("\n[3] 4명 전부: '7번홀 파3 에이 3 비 4 씨 5 디 6'")
r = parse_voice_text("7번홀 파3 에이 3 비 4 씨 5 디 6")
check("hole_number", r.get("hole_number"), 7)
check("par", r.get("par"), 3)
check("score_a", r["scores"].get("score_a"), 3)
check("score_b", r["scores"].get("score_b"), 4)
check("score_c", r["scores"].get("score_c"), 5)
check("score_d", r["scores"].get("score_d"), 6)

# ── 4. 영문 소문자 ──────────────────────────────────────
print("\n[4] 영문 소문자: '18번홀 파4 a 5 b 4 c 3 d 6'")
r = parse_voice_text("18번홀 파4 a 5 b 4 c 3 d 6")
check("hole_number", r.get("hole_number"), 18)
check("par", r.get("par"), 4)
check("score_a", r["scores"].get("score_a"), 5)
check("score_b", r["scores"].get("score_b"), 4)
check("score_c", r["scores"].get("score_c"), 3)
check("score_d", r["scores"].get("score_d"), 6)

# ── 5. 타수 키워드 ──────────────────────────────────────
print("\n[5] '타수' 키워드: '5번홀 파4 에이 타수 4'")
r = parse_voice_text("5번홀 파4 에이 타수 4")
check("hole_number", r.get("hole_number"), 5)
check("score_a", r["scores"].get("score_a"), 4)

# ── 6. 홀만 (스코어 없음) ───────────────────────────────
print("\n[6] 홀만: '12번홀 파3'")
r = parse_voice_text("12번홀 파3")
check("hole_number", r.get("hole_number"), 12)
check("par", r.get("par"), 3)
check("scores empty", r["scores"], {})

# ── 7. mock_stt ─────────────────────────────────────────
print("\n[7] mock_stt -> parse_voice_text 연동")
text = mock_stt(b"dummy audio")
r = parse_voice_text(text)
check("mock text", text, "1번홀 파4 에이 스코어 5 비 4타")
check("hole_number", r.get("hole_number"), 1)
check("par", r.get("par"), 4)
check("score_a", r["scores"].get("score_a"), 5)
check("score_b", r["scores"].get("score_b"), 4)

# ── 8. 번홀 vs 번 홀 (공백) ─────────────────────────────
print("\n[8] 공백 변형: '2번 홀 파4 에이 스코어 3'")
r = parse_voice_text("2번 홀 파4 에이 스코어 3")
check("hole_number", r.get("hole_number"), 2)
check("score_a", r["scores"].get("score_a"), 3)

# ── 9. '시' → score_c ──────────────────────────────────
print("\n[9] '시' 매핑: '4번홀 파4 시 5'")
r = parse_voice_text("4번홀 파4 시 5")
check("score_c", r["scores"].get("score_c"), 5)

# ── Summary ─────────────────────────────────────────────
print("\n" + "=" * 60)
total = PASS + FAIL
print(f"Result: {PASS}/{total} passed, {FAIL} failed")
if FAIL == 0:
    print("All tests PASSED!")
else:
    print(f"{FAIL} test(s) FAILED")
    sys.exit(1)
