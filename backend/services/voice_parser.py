import re
import time
from typing import Dict, Any, Optional

def parse_voice_text(text: str, par_hint: int = 4) -> Dict[str, Any]:
    """
    음성 인식 결과 텍스트를 파싱하여 홀 정보와 스코어를 추출합니다.
    사용자가 말한 순서대로 숫자만 추출하여 플레이어 A, B, C, D 순서로 할당합니다.
    예: "0 1 -1 2" -> A:0, B:1, C:-1, D:2
    숫자 범위: -1 ~ 5
    """
    print(f"Parsing voice text: {text}")
    result = {"scores": {}}
    
    # 텍스트 전처리: 한글 음수 및 숫자 표현 정규화
    t = text.lower().strip()
    
    # 영어 표현도 처리
    t = t.replace('minus', '-').replace('plus', '+')
    t = t.replace('마이너스', '-').replace('빼기', '-').replace('마이나스', '-')
    t = t.replace('마이너 스', '-').replace('마이 너스', '-')  # 분리 인식
    t = t.replace('플러스', '+').replace('더하기', '+')
    t = t.replace('제로', '0').replace('이븐', '0').replace('even', '0')
    
    # 골프 용어 → 숫자 변환 (par 기준 상대값)
    t = t.replace('더블보기', '+2').replace('트리플보기', '+3')
    t = t.replace('보기', '+1').replace('버디', '-1').replace('이글', '-2')
    t = t.replace('bogey', '+1').replace('birdie', '-1').replace('eagle', '-2')
    t = t.replace('double bogey', '+2').replace('triple bogey', '+3')

    # 마이너스 기호 뒤의 공백 제거 ("- 1" -> "-1", "- 일" -> "-일")
    t = re.sub(r'-\s+', '-', t)
    # 플러스 기호 뒤의 공백 제거
    t = re.sub(r'\+\s+', '+', t)
    
    # 한글 숫자 오인식 보정
    # 숫자 매핑 테이블 (오인식 단어 대거 추가)
    kor_num_map = {
        '영': '0', '공': '0', '빵': '0', '병': '0', '용': '0', '형': '0', '엉': '0', '명': '0', '정': '0', '경': '0', '현': '0', '파': '0', '팔': '0',
        '일': '1', '인': '1', '실': '1', '일번': '1', '임': '1', '일은': '1', '한': '1', '하나': '1',
        '이': '2', '리': '2', '이는': '2', '둘': '2', '두': '2',
        '삼': '3', '산': '3', '상': '3', '셋': '3', '세': '3',
        '사': '4', '사는': '4', '넷': '4', '네': '4',
        '오': '5', '어': '5', '오는': '5', '다섯': '5'
    }
    
    # 1. 명시적인 숫자(아라비아 숫자) 먼저 찾기
    numbers = re.findall(r'-?\d+', t)
    
    # 2. 숫자가 안 찾아졌거나 부족한 경우, 한글 발음 기반 매핑 시도
    if not numbers or len(numbers) < 4:
        # 텍스트에서 - 기호 보존하면서 한글/영문자 등을 매핑
        mapped_text = ""
        is_negative = False
        
        for char in t:
            if char == '-':
                is_negative = True
            elif char.isdigit():
                if is_negative:
                    mapped_text += f"-{char} "
                    is_negative = False
                else:
                    mapped_text += f"{char} "
            elif char in kor_num_map:
                val = kor_num_map[char]
                if is_negative:
                    mapped_text += f"-{val} "
                    is_negative = False
                else:
                    mapped_text += f"{val} "
            else:
                # 공백이나 기타 문자는 무시하되 음수 플래그 리셋 여부 결정
                if char.isspace():
                    pass # 공백은 무시
                
        print(f"  Mapped text: {mapped_text}")
        # 다시 숫자 추출
        numbers = re.findall(r'-?\d+', mapped_text)

    # 추출된 숫자 중 유효 범위 (-1 ~ 5) 필터링
    valid_scores = []
    for n in numbers:
        val = int(n)
        if -2 < val < 10: # 유효 범위 필터링 (-1 ~ 9까지 여유 있게 허용 후 최종 제한)
            valid_scores.append(val)
            
    print(f"  Extracted valid scores: {valid_scores}")

    # 플레이어 순서대로 할당 (A, B, C, D)
    players = ['score_a', 'score_b', 'score_c', 'score_d']
    for i, score in enumerate(valid_scores):
        if i < len(players):
            # 골프 스코어 상한/하한 적용 (-1 ~ 5)
            final_val = max(-1, min(5, score))
            result['scores'][players[i]] = final_val
            print(f"  Assigned {players[i]}: {final_val}")
            
    return result

def mock_stt(audio_bytes: bytes) -> str:
    """
    개발용 Mock STT 서비스
    """
    print(f"Mock STT received {len(audio_bytes)} bytes of audio.")
    time.sleep(1.5)
    return "0 1 -1 2"
